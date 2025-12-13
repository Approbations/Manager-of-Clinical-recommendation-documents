from fastapi import APIRouter, HTTPException, Form, File, UploadFile, Query, Depends
from services.document_service import DocumentService
from services.user_service import UserService
from docs_processing.pageable import Pageable, PaginatedResponse
from auth.dependencies import require_admin_role, require_client_role


page_router = APIRouter()


@page_router.get("/")
async def root():
    return {
        "status": "ok",
        "message": "WebSocket чат доступен по /ws/chat"
    }


@page_router.get("/doclist/paginated")  # получение всех документов с пагинацией
async def get_docs_paginated(
        page: int = Query(0, ge=0, description="Номер страницы (начинается с 0)"),
        size: int = Query(10, ge=1, le=100, description="Размер страницы (1-100)")
):
    docs = DocumentService.get_all_docs(page=page, size=size)
    total = DocumentService.get_total_documents()

    return PaginatedResponse(
        items=docs,
        total=total,
        pageable=Pageable(page=page, size=size),
        total_pages=(total + size - 1) // size
    )


@page_router.delete("/doclist/{doc_id}")  # удаление документа по id
async def delete_doc(doc_id: str, current_user=Depends(require_admin_role)):
    if not DocumentService.delete_doc(doc_id):
        raise HTTPException(status_code=404, detail="Файл для удаления не найден")


@page_router.get("/doclist/{doc_id}")  # скачивание документа по id
async def get_doc_id(doc_id: str):
    document = DocumentService.get_doc(doc_id)
    if document:
        return document
    raise HTTPException(status_code=404, detail="Файл не найден")


@page_router.post("/createdoc")  # загрузка нового документа
async def upload_doc(doc_id: str = Form(..., description="ID документа"),
                     title: str = Form(..., description="Навзвание документа"),
                     mcb: str = Form("NULL", description="МКБ-10"),
                     age_category: str = Form("Взрослые", description="Возрастная категория"),
                     developer: str = Form("NULL", description="Разработчик"),
                     creator: str = Form("Минздрав", description="Загрузил файл"),
                     file: UploadFile = File(..., description="PDF файл"),
                     current_user=Depends(require_admin_role)):
    '''достать логин из поьзователя'''
    user_login = creator if creator == "Минздрав" else str(current_user.login)
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Неправильный формат файла")

    file_data = await file.read()
    try:
        DocumentService.create_doc(doc_id, title, mcb, age_category, developer, user_login, file_data)
        return {
            "message": "Новый документ загружен",
            "doc_id": doc_id,
            "title": title,
            "MCB": mcb,
            "age_category": age_category,
            "developer": developer,
            "creator": user_login
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка в загрузке документе: {str(e)}")


@page_router.get("/get_my_docs")  # олучение всех документов загруженных пользователем
async def get_my_docs(
        page: int = Query(0, ge=0, description="Номер страницы (начинается с 0)"),
        size: int = Query(10, ge=1, le=100, description="Размер страницы (1-100)"),
        current_user=Depends(require_client_role)):
    docs = DocumentService.get_my_docs(page=page, size=size, creator=current_user.login)
    total = len(docs)

    return PaginatedResponse(
        items=docs,
        total=total,
        pageable=Pageable(page=page, size=size),
        total_pages=(total + size - 1) // size
    )


@page_router.post("/createmydoc")  # загрузка нового документа пользоватлем
async def upload_my_doc(doc_id: str = Form(..., description="ID документа"),
                        title: str = Form(..., description="Навзвание документа"),
                        mcb: str = Form("NULL", description="МКБ-10"),
                        age_category: str = Form("Взрослые", description="Возрастная категория"),
                        developer: str = Form("NULL", description="Разработчик"),
                        file: UploadFile = File(..., description="PDF файл"),
                        current_user=Depends(require_client_role)):
    '''достать логин из поьзователя'''
    user_login = str(current_user.login)
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Неправильный формат файла")

    file_data = await file.read()
    try:
        DocumentService.create_doc(doc_id, title, mcb, age_category, developer, user_login, file_data)
        return {
            "message": "Новый документ загружен",
            "doc_id": doc_id,
            "title": title,
            "MCB": mcb,
            "age_category": age_category,
            "developer": developer,
            "creator": user_login
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка в загрузке документе: {str(e)}")


@page_router.delete("/mydoclist/{doc_id}")  # удаление документа по id у клиента
async def delete_my_doc(doc_id: str, current_user=Depends(require_client_role)):
    login = current_user.login
    if not DocumentService.delete_my_doc(doc_id=doc_id, login=login):
        raise HTTPException(status_code=404, detail="Файл для удаления не найден")


@page_router.post("/profile")  # изменение имени пользователя
async def change_profile(first_name: str, last_name: str, current_user=Depends(require_client_role)):
    login = current_user.login
    if not UserService.change_profile(first_name, last_name, login):
        raise HTTPException(status_code=304, detail="Не получается изменить данные")


@page_router.get("/profiles")  # получением данных пользователей
async def get_profiles(
        page: int = Query(0, ge=0, description="Номер страницы (начинается с 0)"),
        size: int = Query(10, ge=1, le=100, description="Размер страницы (1-100)")):
    accounts = DocumentService.get_profiles(page=page, size=size)
    total = len(accounts)

    return PaginatedResponse(
        items=accounts,
        total=total,
        pageable=Pageable(page=page, size=size),
        total_pages=(total + size - 1) // size
    )


@page_router.get("/profile")  # получение пользователя по логину
async def get_user_profile(login):
    account = UserService.get_user_profile(login)
    if account:
        return account
    raise HTTPException(status_code=404, detail="Не найден аккаунт")
