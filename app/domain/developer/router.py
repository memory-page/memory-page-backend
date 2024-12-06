from fastapi import APIRouter

router = APIRouter()

@router.get("/developer")
async def get_developers():
    # 임시 데이터
    sponsor_account = {
        "bank": "국민은행",
        "account_number": "123-456-789",
        "account_holder": "memory-page"
    }
    developers = [
        {
            "name": "강민서",
            "github": "https://github.com/mseo39"
        },
        {
            "name": "이인규",
            "github": "https://github.com/DevelopLee20"
        },
        {
            "name": "김정훈",
            "github": "https://github.com/jeong011010"
        },
        {
            "name": "박지우",
            "github": "https://github.com/jiwoopark727"
        },
    ]
    contact_email = "kang20@sch.ac.kr"
    return {"developers": developers, "sponsor_account": sponsor_account, "contact_email": contact_email}
