from typing import List
from fastapi import FastAPI, HTTPException

from datetime import datetime
from models import AdvertisementUpdate, Advertisement, AdvertisementCreate

app = FastAPI(
    title="Ads"
)

ads = {}
next_id = 1

@app.post('/advertisement', response_model=Advertisement, status_code=201)
async def create_ad(ad: AdvertisementCreate):
    global next_id
    ad = Advertisement(
        id=next_id,
        created_at=datetime.utcnow(),
        **ad.dict()
    )
    ads[next_id] = ad
    next_id += 1
    return ad

@app.get('/advertisement/{ad_id}')
def get_ad(ad_id: int):
    ad = ads.get(ad_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Объявление не найдено")
    return ad

@app.delete('/advertisement/{ad_id}', status_code=204)
def delete_ad(ad_id: int):
    if ad_id not in ads:
        raise HTTPException(status_code=404, detail="Объявление не найдено")
    del ads[ad_id]

@app.patch('/advertisement/{ad_id}', response_model=Advertisement)
def update_ad(ad_id: int, ad_update: AdvertisementUpdate):
    ad = ads.get(ad_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Объявление не найдено")
    update_data = ad_update.dict(exclude_unset=True)
    update_ad = ad.copy(update=update_data)
    ads[ad_id] = update_ad
    return update_ad

@app.get('/advertisement', response_model=List[Advertisement])
def search_ads(
    title: str = None,
    owner: str = None,
    price: float = None
):
    result = list(ads.values())
    if title:
        result = [ad for ad in result if title.lower() in ad.title.lower()]
    if owner:
        result = [ad for ad in result if owner.lower() in ad.owner.lower()]
    if price is not None:
        result = [ad for ad in result if ad.price == price]

    return result