from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

# 路径参数： item_id 是路径参数，q 是查询参数
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

# 查询参数： q 是查询参数
# e.g., http://localhost:8000/items/?q=test
@app.get("/items/")
def read_items(q: str = None):
    return {"q": q}

# 数据模型：
class Item(BaseModel):
    name: str
    description: str = None

# 对应的请求体（JSON）：
# {
#     "name": "test",
#     "description": "test description"
# }

@app.post("/items/")
def create_item(item: Item):
    return item

# Query: 额外的校验
from fastapi import Query

# q是可选参数（Query的第一个参数是默认值），如果设置了q，则进行校验 -> min_length=3, max_length=50
@app.get("/items/")
async def read_items(q: str = Query(None, min_length=3, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# q是必填参数，且min_length=3, max_length=50
@app.get("/items/")
async def read_items(q: str = Query(..., min_length=3, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


from typing import Union, List
# 用Query接收list
# http://localhost:8000/items/?q=foo&q=bar
# 响应：
# {
#     "q": ["foo", "bar"]
# }
@app.get("/items/")
async def read_items(q: Union[List[str], None] = Query(None)):
    query_items = {"q": q}
    return query_items


# 用Query接收list，且有默认值
@app.get("/items/")
async def read_items(q: List[str] = Query(["foo", "bar"])):
    query_items = {"q": q}
    return query_items


# 用Query声明更多元数据
@app.get("/items/")
async def read_items(
    q: Union[str, None] = Query(
        None,
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,   
        deprecated=True, # 提示用户已弃用    
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 别名参数
# 指定查询参数为 item-query
# http://127.0.0.1:8000/items/?item-query=foobaritems
# 在Query中指定alias="item-query"
@app.get("/items/")
async def read_items(q: str = Query(..., alias="item-query")): # ...表示必填
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 使用Path为路径参数声明校验与元数据
from fastapi import Path
@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(..., title="item ID to get", ge=0, le=1000), # ge=0, le=1000表示最小值为0，最大值为1000
    q: str = Query(None, alias="item-query"),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


# 使用Pydantic模型声明查询参数
from typing import Literal, Annotated
from pydantic import BaseModel, Field

# 使用Field校验请求体内的字段
class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=1000) # 100是默认值，gt=0, le=1000表示最小值为0，最大值为1000
    offset: int = Field(0, ge=0)
    order_dy: Literal["asc", "desc"] = Field(default="asc") # Literal表示只能取"asc"或"desc"

@app.get("/items")
async def read_items(filter_query: Annotated[FilterParams, Query()]): 
    # Annotated用于为参数添加元数据，Query()告诉FastAPI使用Query解析器
    # /items?limit=50&offset=10&order_dy=desc
    return filter_query


# 声明多个请求体
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None


# 期望请求体：
# {
#     "item": {
#         "name": "Foo",
#         "description": "The pretender",
#         "price": 42.0,
#         "tax": 3.2
#     },
#     "user": {
#         "username": "dave",
#         "full_name": "Dave Grohl"
#     }
# }

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results

from fastapi import Body
# 增加单一请求体
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User, importance: Annotated[int, Body()]
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results


# 嵌入请求体
# 当只有一个请求体时，可以保留键在JSON中
# 期望请求体：
# {
#     "item": {
#         "name": "Foo",
#         "description": "The pretender",
#         "price": 42.0,
#         "tax": 3.2
#     }
# }
# 而不是
# {
#     "name": "Foo",
#     "description": "The pretender",
#     "price": 42.0,
#     "tax": 3.2
# }
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results


# 定义子模型
class Image(BaseModel):
    url: str
    name: str

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []
    image: Image | None = None

# 期望请求体：
# {
#     "name": "Foo",
#     "description": "The pretender",
#     "price": 42.0,
#     "tax": 3.2,
#     "tags": ["tag1", "tag2"],
#     "image": {
#         "url": "https://example.com/image.png",
#         "name": "image.png"
#     }
# }

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results


# 用schema_extra声明请求体例子
class Item(BaseModel):
    name: str = Field(examples=["Foo"]) # Field也可以接收examples
    description: str | None = None
    price: float

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "price": 42.0,
                }
            ]
        }
    }

# 定义Cookie参数
from fastapi import Cookie

@app.get("/items/")
async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}


# 定义Header参数
# 默认情况下，Header 把参数名中的字符由下划线（_）改为连字符（-）来提取并存档请求头 。
from fastapi import Header

@app.get("/items/")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"user_agent": user_agent}


# 如果有一组相关的cookie，可以创建Pydantic模型来声明
class Cookies(BaseModel):
    model_confg = {"extra": "forbid"} # 不接受额外的cookie

    session_id: str
    tracker: str | None = None

# FastAPI 将从请求中接收到的 cookie 中提取出每个字段的数据
@app.get("/items/")
async def read_items(cookies: Annotated[Cookies, Cookie()]):
    return cookies


# 如果有一组相关的header，可以创建Pydantic模型来声明
class Headers(BaseModel):
    user_agent: str
    save_data: bool

@app.get("/items/")
async def read_items(headers: Annotated[Headers, Header()]):
    return headers


# 在路径操作中使用response_model参数来声明返回类型
# 1. 将输出数据转换成声明的类型
# 2. 校验数据
# 3. 生成文档
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/{item_id}", response_model=Item)
async def create_item(item: Item):
    return item


@app.get("/items/", response_model=list[Item])
async def read_items():
    return [
        {"name": "Foo", "description": "There goes my hero"},
        {"name": "Bar", "description": "The blues"},
    ]


items = {
    "foo": {"name": "Foo", "description": "There goes my hero"},
}

# 使用response_model_exclude_unset参数来排除未设置的值
# 返回的JSON中不会包含未设置的值
# {
#   "name": "Foo",
#   "description": "There goes my hero"
# }
@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]


# 响应状态码
# 200: 成功
# 300: 重定向
# 400: 客户端错误
# 500: 服务端错误
@app.post("/items/", status_code=201)
async def create_item(name: str):
    return {"name": name}


# 使用Form接收表单，而非JSON
# 安装： pip install python-multipart
from fastapi import Form

@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}

# 定义表单模型
class FormData(BaseModel):
    username: str
    password: str

@app.post("/login/")
async def login(form_data: FormData = Form(...)):
    return {"username": form_data.username}


# 使用File接收文件
from fastapi import File, UploadFile

@app.post("/files/")
async def create_file(file: bytes = File(...)): # 保存在内存中，适用于小文件
    return {"file_size": len(file)}

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)): # 当内存不够时，会存入磁盘
    return {"filename": file.filename}


# 处理错误
from fastapi import HTTPException

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]


# 路径操作配置
# status_code: 响应状态码
# summary: 路径操作的摘要
# description: 路径操作的描述
# deprecated: 是否弃用
# tags: 路径操作的标签 (在OpenAPI中显示)
# response_model: 响应模型
# ...
# docstring也会显示在OpenAPI中
@app.post(
    "/items/",
    tags=["items"],
    response_model=Item,
    summary="Create an item",
    description="Create an item with all the information, name, description, price, tax and a set of unique tags",
)
async def create_item(item: Item):
    """
    Create an item with all the information, name, description, price, tax and a set of unique tags
    """
    return item


# JSON序列化
# 使用jsonable_encoder函数将数据转换成JSON
from fastapi import jsonable_encoder

fake_db = {}
@app.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data


# 依赖注入
# 场景
# 1. 共享业务逻辑
# 2. 共享数据库连接
# 3. 实现安全、验证、角色权限
# 。。。

from fastapi import Depends

# Depends 接收可调用对象，比如函数
# Fastapi调用common_parameters处理参数q,skip,limit并转换成dict返回给路径操作函数
async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 10):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons

@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons


# 使用类作为依赖
class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/")
async def read_items(commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]): # 第二个CommonQueryParams可以省略
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response


# 嵌套依赖项
def query_extractor(q: Union[str, None] = None):
    return q


def query_or_cookie_extractor(
    q: str = Depends(query_extractor),
    last_query: Union[str, None] = Cookie(default=None),
):
    if not q:
        return last_query
    return q


@app.get("/items/")
async def read_query(query_or_default: str = Depends(query_or_cookie_extractor)):
    return {"q_or_cookie": query_or_default}


# 路径操作装饰器依赖项 dependencies
# 不需要返回值、但仍要执行或解析该依赖项
async def verify_token(x_token: str = Header()):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: str = Header()):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]


# 添加全局依赖项
# 为所有路径操作应用该依赖项
app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])


# 使用yield的依赖项
# FastAPI支持在完成后执行一些额外步骤的依赖项，如建立db连接
async def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()


# OAuth2
# FastAPI 支持 OAuth2 身份验证
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # 客户端的url用于发送username和password，并获取token
@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]): # 依赖项oauth2_scheme向路径操作函数传递了 str 类型的 token
    return {"token": token}


# 更实用的做法：返回当前用户
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]): # 注入oauth2_scheme获取token
    user = fake_decode_token(token)
    return user


@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]): # 注入get_current_user获取用户
    return current_user


# OAuth2 规范要求使用密码流时，客户端或用户必须以表单数据形式发送 username 和 password 字段。
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    return user

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def fake_hash_password(password: str):
    return "fakehashed" + password

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # 通过表单获取账号密码
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    # 校验哈希后的密码
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password: 
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # 返回token
    # 本例只是简单的演示，返回的 Token 就是 username，但这种方式极不安全。
    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


# JWT
# JSON 网络令牌（JSON Web Tokens）
# JWT 是一种将 JSON 对象编码为没有空格，且难以理解的长字符串的标准。
# JWT 字符串没有加密，任何人都能用它恢复原始信息。
# 但 JWT 使用了签名机制。接受令牌时，可以用签名校验令牌。
# 
# pip install pyjwt

# 哈希明文密码
# pip install passlib[bcrypt] 
# https://fastapi.tiangolo.com/zh/tutorial/security/oauth2-jwt/#_6



# 中间件
# "中间件"是一个函数,它在每个请求被特定的路径操作处理之前,以及在每个响应返回之前工作.
import time
from fastapi import FastAPI, Request

# 在函数顶部实用装饰器@app.middleware("http")
# 中间件参数接收如下参数:
# 1. request
# 2. 一个函数 call_next 它将接收 request 作为参数
# 然后你可以在返回 response 前进一步修改它.
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response



# 管理应用
# ├── app                  # 「app」是一个 Python 包
# │   ├── __init__.py      # 这个文件使「app」成为一个 Python 包
# │   ├── main.py          # 「main」模块，例如 import app.main
# │   ├── dependencies.py  # 「dependencies」模块，例如 import app.dependencies
# │   └── routers          # 「routers」是一个「Python 子包」
# │   │   ├── __init__.py  # 使「routers」成为一个「Python 子包」
# │   │   ├── items.py     # 「items」子模块，例如 import app.routers.items
# │   │   └── users.py     # 「users」子模块，例如 import app.routers.users
# │   └── internal         # 「internal」是一个「Python 子包」
# │       ├── __init__.py  # 使「internal」成为一个「Python 子包」
# │       └── admin.py     # 「admin」子模块，例如 import app.internal.admin


# app/routers/users.py
# 专门用于处理用户逻辑
from fastapi import APIRouter

router = APIRouter()

@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}


# app/dependencies.py
# 管理依赖项
from fastapi import Header, HTTPException
async def get_token_header(x_token: str = Header()):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")
    

# app/routers/items.py
# 专门用于处理物品逻辑
# 因为所有路径操作都有相同的prefix, tags, 额外response，dependencies
# 可以通过APIRouter在定义prefix，dependencies...来简化代码
router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}

@router.get("/")
async def read_items():
    return fake_items_db


@router.get("/{item_id}")
async def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_items_db[item_id]["name"], "item_id": item_id}


@router.put(
    "/{item_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}

# app/main.py
from fastapi import Depends, FastAPI

from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, users

app = FastAPI(dependencies=[Depends(get_query_token)])


app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}



# 后台任务
# 你可以定义在返回响应后运行的后台任务。
# 这对需要在请求之后执行的操作很有用，但客户端不必在接收响应之前等待操作完成。
# 如：
# 1. 执行操作后发送的电子邮件通知
# 2. 处理数据
from fastapi import BackgroundTasks, FastAPI

def write_notification(email: str, message=""): # 后台执行的函数
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks): # 定义后台任务参数
    background_tasks.add_task(write_notification, email, message="some notification") # 添加后台任务
    return {"message": "Notification sent in the background"}