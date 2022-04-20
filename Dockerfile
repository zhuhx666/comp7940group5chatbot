FROM python
COPY ProjectChatbot.py ./
COPY requirements.txt ./
COPY chatbot-cf4ce-firebase-adminsdk-t6b1e-25d55c8560.json ./
EXPOSE 80
RUN pip install pip update
RUN pip install -r requirements.txt
ENV ACCESS_TOKEN=5105224852:AAGpK2FUHJe8zyx9sIVBYCf4-q-qlukaZSs
CMD python chatbot.py