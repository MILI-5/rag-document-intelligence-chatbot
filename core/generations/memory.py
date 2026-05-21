from langchain.memory import ConversationBufferWindowMemory


def get_memory():

    memory = ConversationBufferWindowMemory(
        k=5,
        memory_key="chat_history",
        return_messages=True
    )

    return memory