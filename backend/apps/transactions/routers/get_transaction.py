from apps.transactions.routers import router


@router.get("/init")
async def get_transactions():
    return {"message": "List of transactions"}
