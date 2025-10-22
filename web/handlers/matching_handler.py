from aiohttp import web
from ..middlewares import middleware, semaphore
from database.methods.products import get_all_products
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import logging

logger = logging.getLogger(__name__)

@middleware(semaphore(10, 10))
async def matching_handler(request: web.Request) -> web.Response:
    logger.debug("Matching handler called")
    s = request.rel_url.query.get("s", "")
    if not s:
        logger.debug("Missing query parameter 's'")
        return web.json_response({"error": "missing query parameter 's'"}, status=400)

    db = request.app["db"]
    session = db.session
    try:
        logger.debug(f"Processing matching request for query: {s}")
        products = get_all_products(session)
        if not products:
            logger.debug("No products found in database")
            return web.json_response({"query": s, "ranked_products": []})

        product_texts = [f"{p['title']} {p['description']}" for p in products]
        logger.debug(f"Vectorizing {len(product_texts)} product texts")
        vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        product_vecs = vectorizer.fit_transform(product_texts)
        query_vec = vectorizer.transform([s])
        sims = cosine_similarity(query_vec, product_vecs)[0]
        ranked_idx = np.argsort(-sims)
        
        ranked = []
        
        for i in ranked_idx:
            if (score := float(sims[i]))!=0:
                ranked.append({"product_id": int(products[i]["id"]), 
                   "product_title": str(products[i]["title"]),
                   "product_desc": str(products[i]["description"]),
                   "score": score})

        logger.debug(f"Matching completed, found {len(ranked)} relevant products")
        return web.json_response({"query": s, "ranked_products": ranked})
    except Exception as e:
        logger.error(f"Error in matching handler: {str(e)}")
        return web.json_response({"error": "internal server error"}, status=500)
    finally:
        session.close()