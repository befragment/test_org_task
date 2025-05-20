import asyncio
from models import Building, Activity, Organization
from database import async_session_maker, Base, engine

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def create_mock_data():
    await init_db()

    async with async_session_maker() as session:
        buildings = [
            Building(id=1, address='Lenina 1', latitude=55.751244, longitude=37.618423),
            Building(id=2, address='Tverskaya 10', latitude=55.764, longitude=37.609),
        ]
        session.add_all(buildings)

        activities = [
            Activity(id=1, name='Еда', parent_id=None),
            Activity(id=2, name='Мясная продукция', parent_id=1),
            Activity(id=3, name='Молочная продукция', parent_id=1),
            Activity(id=4, name='Ремонт', parent_id=None),
        ]
        session.add_all(activities)

        await session.commit()  

        org1 = Organization(id=1, name='Мясной магазин', phone_numbers=['+7 123 456 7890'], building_id=1)
        org1.activities.append(activities[1]) 

        org2 = Organization(id=2, name='Молочная лавка', phone_numbers=['+7 234 567 8901'], building_id=1)
        org2.activities.append(activities[2])

        org3 = Organization(id=3, name='Кафе', phone_numbers=['+7 345 678 9012'], building_id=2)
        org3.activities.append(activities[0])

        org4 = Organization(id=4, name='Автосервис', phone_numbers=['+7 456 789 0123'], building_id=2)
        org4.activities.append(activities[3])

        session.add_all([org1, org2, org3, org4])
        await session.commit()

if __name__ == '__main__':
    asyncio.run(create_mock_data())
