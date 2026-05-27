from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from app.db import get_db_connection
import json

async def get_cards(request):
    query_param = request.query_params.get('q', '').strip()
    conn = get_db_connection()
    if conn is None:
        return JSONResponse({"error": "Database connection failed"}, status_code=500)
    try:
        cur = conn.cursor()
        if query_param:
            sql = "SELECT id, name, issuer, image_url FROM cards WHERE name ILIKE %s OR issuer ILIKE %s"
            cur.execute(sql, (f'%{query_param}%', f'%{query_param}%'))
        else:
            sql = "SELECT id, name, issuer, image_url FROM cards"
            cur.execute(sql)
        cards = cur.fetchall()
        cur.close()
        conn.close()
        for card in cards:
            if isinstance(card, dict) and 'id' in card:
                card['id'] = str(card['id'])
        return JSONResponse(cards)
    except Exception as e:
        if conn: conn.close()
        return JSONResponse({"error": str(e)}, status_code=500)

async def get_user_cards(request):
    conn = get_db_connection()
    if conn is None:
        return JSONResponse({"error": "Database connection failed"}, status_code=500)
    try:
        cur = conn.cursor()
        # Join with cards table to get full details
        sql = """
            SELECT uc.id as association_id, c.id, c.name, c.issuer, c.image_url 
            FROM user_cards uc
            JOIN cards c ON uc.card_id = c.id
        """
        cur.execute(sql)
        user_cards = cur.fetchall()
        cur.close()
        conn.close()
        for item in user_cards:
            if isinstance(item, dict):
                item['id'] = str(item['id'])
                item['association_id'] = str(item['association_id'])
        return JSONResponse(user_cards)
    except Exception as e:
        if conn: conn.close()
        return JSONResponse({"error": str(e)}, status_code=500)

async def add_user_card(request):
    try:
        body = await request.json()
        card_id = body.get('card_id')
    except Exception:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)
    
    if not card_id:
        return JSONResponse({"error": "card_id is required"}, status_code=400)
        
    conn = get_db_connection()
    if conn is None:
        return JSONResponse({"error": "Database connection failed"}, status_code=500)
    
    try:
        cur = conn.cursor()
        
        # 1. Validate card exists
        cur.execute("SELECT id FROM cards WHERE id = %s", (card_id,))
        if not cur.fetchone():
            cur.close()
            conn.close()
            return JSONResponse({"error": "Card not found in master library"}, status_code=404)
            
        # 2. Check for duplicates
        cur.execute("SELECT id FROM user_cards WHERE card_id = %s", (card_id,))
        if cur.fetchone():
            cur.close()
            conn.close()
            return JSONResponse({"error": "Card already in inventory"}, status_code=409)
            
        # 3. Insert
        cur.execute("INSERT INTO user_cards (card_id) VALUES (%s) RETURNING id", (card_id,))
        new_id = cur.fetchone()['id']
        conn.commit()
        cur.close()
        conn.close()
        
        return JSONResponse({"id": str(new_id), "card_id": str(card_id)}, status_code=201)
    except Exception as e:
        if conn: conn.close()
        return JSONResponse({"error": str(e)}, status_code=500)

async def delete_user_card(request):
    assoc_id = request.path_params.get('id')
    conn = get_db_connection()
    if conn is None:
        return JSONResponse({"error": "Database connection failed"}, status_code=500)
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM user_cards WHERE id = %s", (assoc_id,))
        deleted_count = cur.rowcount
        conn.commit()
        cur.close()
        conn.close()
        
        if deleted_count == 0:
            return JSONResponse({"error": "Association not found"}, status_code=404)
        return JSONResponse(None, status_code=204)
    except Exception as e:
        if conn: conn.close()
        return JSONResponse({"error": str(e)}, status_code=500)

routes = [
    Route("/api/cards", get_cards, methods=["GET"]),
    Route("/api/user/cards", get_user_cards, methods=["GET"]),
    Route("/api/user/cards", add_user_card, methods=["POST"]),
    Route("/api/user/cards/{id}", delete_user_card, methods=["DELETE"])
]

app = Starlette(debug=True, routes=routes)
