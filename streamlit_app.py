
import streamlit as st
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup
DATABASE_URL = 'sqlite:///database.db'
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()

class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    content = Column(String(200), nullable=False)
    done = Column(Boolean, default=False)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Streamlit App
st.title("📝 Simple To-Do List App with Streamlit")

# Add Task
with st.form(key='add_task_form'):
    new_task = st.text_input("Enter a new task:")
    submit = st.form_submit_button("Add Task")

    if submit and new_task.strip():
        task = Task(content=new_task.strip(), done=False)
        session.add(task)
        session.commit()
        st.success(f"Added task: {new_task}")

# Show all tasks
tasks = session.query(Task).all()

for task in tasks:
    cols = st.columns([5, 1, 1])
    cols[0].write(f"✅ {task.content}" if task.done else task.content)
    if cols[1].button("Toggle", key=f"toggle-{task.id}"):
        task.done = not task.done
        session.commit()
        st.experimental_rerun()
    if cols[2].button("Delete", key=f"delete-{task.id}"):
        session.delete(task)
        session.commit()
        st.experimental_rerun()
