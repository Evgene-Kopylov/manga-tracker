from db.models import Page
from db.session import SessionLocal

session = SessionLocal()


def cleare_db():
    pages = session.query(Page).all()
    print(len(pages))
    for page in pages:
        if page.total == 0 and page.parsing_start:
            session.delete(page)
    session.commit()


if __name__ == "__main__":
    cleare_db()
