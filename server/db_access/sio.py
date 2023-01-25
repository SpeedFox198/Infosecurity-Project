from sqlalchemy.exc import SQLAlchemyError

from db_access.globals import async_session
import sqlalchemy as sa

from models import (
    User,
    SioConnection,
    FriendRequest,
    Friend, Room, Membership
)


async def set_online_status(user_id: str, status: bool) -> None:
    async with async_session() as session:
        try:
            statement = sa.update(User).where(User.user_id == user_id).values(online=status)
            await session.execute(statement)
            await session.commit()
        except SQLAlchemyError:
            await session.rollback()


async def add_sio_connection(sid: str, user_id: str) -> None:
    async with async_session() as session:
        connection_exists_statement = sa.select(SioConnection).where(
            (SioConnection.user_id == user_id)
        )
        connection_exists = (await session.execute(connection_exists_statement)).scalar()
        if not connection_exists:
            session.add(SioConnection(sid, user_id))
            await session.commit()
            return

        check_diff_sid_statement = sa.select(SioConnection).where(
            (SioConnection.sid != sid) &
            (SioConnection.user_id == user_id)
        )
        diff_sid_connection: SioConnection | None = (await session.execute(check_diff_sid_statement)).scalar()

        if diff_sid_connection:
            try:
                update_sid_statement = sa.update(SioConnection)\
                    .where(SioConnection.user_id == diff_sid_connection.user_id)\
                    .values(sid=sid)
                await session.execute(update_sid_statement)
                await session.commit()
            except SQLAlchemyError:
                await session.rollback()


async def remove_sio_connection(sid: str, user_id: str) -> None:
    async with async_session() as session:
        try:
            statement = sa.delete(SioConnection).where(
                (SioConnection.sid == sid) & (SioConnection.user_id == user_id)
            )
            await session.execute(statement)
            await session.commit()
        except SQLAlchemyError:
            await session.rollback()


async def get_sid_from_sio_connection(user_id: str) -> str | None:
    async with async_session() as session:
        statement = sa.select(SioConnection.sid).where(SioConnection.user_id == user_id)
        result = (await session.execute(statement)).scalar()
        return result


async def have_relationship(relationship: list[str, str] | tuple[str, str]) -> Friend | None:
    async with async_session() as session:
        statement = sa.select(Friend).where(
            Friend.user1_id.in_(relationship) &
            Friend.user2_id.in_(relationship)
        )
        return (await session.execute(statement)).one_or_none()


async def remove_friend_request(sender_user_id: str, recipient_user_id: str) -> None:
    async with async_session() as session:
        statement = sa.delete(FriendRequest).where(
            (FriendRequest.sender == sender_user_id) &
            (FriendRequest.recipient == recipient_user_id)
        )
        await session.execute(statement)
        await session.commit()


async def have_public_key(user_id: str) -> bool:
    async with async_session() as session:
        statement = sa.select(User.public_key).where(
            User.user_id == user_id
        )
        result = (await session.execute(statement)).scalar()
        return bool(result)


async def has_disappearing(user_id: str) -> bool:
    async with async_session() as session:
        statement = sa.select(User.disappearing).where(
            User.user_id == user_id
        )
        result = (await session.execute(statement)).scalar()
        print("has disappearing", result)
        return bool(result)


async def get_existing_room(relationship: list[str, str] | tuple[str, str]) -> Room | None:
    print("\n\nChecking existing room...\n\n")
    async with async_session() as session:
        subquery = sa.select(Membership.room_id).where(
            Membership.user_id.in_(relationship)
        ).group_by(Membership.room_id)\
            .having(sa.func.count(Membership.room_id) == 2)\
            .alias("membership_room_id")

        print(subquery)
        statement = sa.select(Room).join(subquery, Room.room_id == subquery.c.room_id).where(
            (Room.type == "direct")
        )
        result: Room | None = (await session.execute(statement)).one_or_none()
        return result
