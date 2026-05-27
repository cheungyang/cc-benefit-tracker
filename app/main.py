from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from app.db import get_db_connection

async def get_cards(request):
    query_param = request.query_params.get('q', '').strip()
    
    conn = get_db_connection()
    if conn is None:
        return JSONResponse({"error": "Database connection failed"}, status_code=500)
    
    try:
        cur = conn.cursor()
        if query_param:
            # Case-insensitive partial match
            sql = "SELECT id, name, issuer, image_url FROM cards WHERE name ILIKE %s OR issuer ILIKE %s"
            cur.execute(sql, (f'%{query_param}%', f'%{query_param}%'))
        else:
            sql = "SELECT id, name, issuer, image_url FROM cards"
            cur.execute(sql)
        
        cards = cur.fetchall()
        cur.close()
        conn.close()
        
        # Ensure UUIDs are strings for JSON serialization
        for card in cards:
            if isinstance(card, dict) and 'id' in card:
                card['id'] = str(card['id'])
                
        return JSONResponse(cards)
    except Exception as e:
        if conn:
            conn.close()
        return JSONResponse({"error": str(e)}, status_code=500)

routes = [
    Route("/api/cards", get_cards, methods=["GET"])
]

app = Starlette(debug=True, routes=routes)
