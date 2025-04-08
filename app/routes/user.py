from fastapi import APIRouter, HTTPException, Path, Depends
from app.types.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.database import get_db
from app.db.models.user import User as UserModel

router = APIRouter()
users = []

# route to create a user
@router.post("/users")
def create_user(user: User):
    for existing_user in users:
        if existing_user.name == user.name:
            raise HTTPException(status_code=400, detail=f"User already exists with userid={existing_user.userid}.")

    userid = 101
    if users:
        userid = users[-1].userid + 1 if users[-1] is not None else 101
    else:
        userid = 101

    user.userid = userid
    users.append(user)

    return {"message": f"User {user.name} created", "user": user}

# route to retrieve all users
@router.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserModel))
    users = result.scalars().all()
    return users

# route to retrieve a user
@router.get("/users/{user_id}")
def get_user(user_id: int = Path(..., title="ID of the user", gt=0, description="User ID between 1 and 1000")):
    try:
        userIndex = lookForUserIndexByUserID(users, user_id)
        if userIndex < 0:
            raise IndexError("User not found")
        else:
            return {"user": users[userIndex]}
    except IndexError:
        print(f"Caught an error: {IndexError}")
        raise HTTPException(status_code=404, detail="User not found.")
    except Exception as e:
        raise HTTPException(status_code=500, details=f"Unexpected error : {str(e)}")    


# route to remove a user
@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    try:
        userIndex = lookForUserIndexByUserID(users, user_id)
        if userIndex < 0:
            raise IndexError("User not found")
        else:
            removed_user = users.pop(userIndex)
            return {"message": "User removed", "user": removed_user}
    except IndexError:
        print(f"Caught an error: {IndexError}")
        raise HTTPException(status_code=404, detail="User not found.")
    except Exception as e:
        raise HTTPException(status_code=500, details=f"Unexpected error : {str(e)}")
    

# route to update a user
@router.put("/users/{user_id}")
def update_user(user_id: int, updated_user: User):
    try:
        userIndex = lookForUserIndexByUserID(users, user_id)
        updated_user.userid = user_id
        users[userIndex] = updated_user

        return {"message": "User updated", "user": updated_user}
    except IndexError:
        print(f"Caught an error: {IndexError}")
        raise HTTPException(status_code=404, detail="User not found.")
    except Exception as e:
        raise HTTPException(status_code=500, details=f"Unexpected error : {str(e)}")

def lookForUserIndexByUserID(users, user_id):
    userFound = False
    for index, user in enumerate(users):
        if user and user.userid == user_id:
            userFound = True
            break
    
    if userFound:
        return index
    else:
        return -1
