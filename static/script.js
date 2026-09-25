const input = document.getElementById("msg");
const sendBtn = document.getElementById("sendBtn");

const API_URL = "https://business-ai-agent-i8wh.onrender.com";

let conversationId = null;


async function loadConversations() {
    try {
        const res = await fetch(
            `${API_URL}/conversations`
        );

        const conversations = await res.json();

        const conversationList =
            document.getElementById("conversationList");

        conversationList.innerHTML = "";

        const newChat = document.createElement("button");

        newChat.textContent = "+ New Chat";
        newChat.className = "new-chat";

        newChat.addEventListener("click", async () => {
            await createConversation();

            document.getElementById("chatBox").innerHTML = "";

            await loadConversations();
        });

        conversationList.appendChild(newChat);


        conversations.forEach((conversation) => {

            const container =
                document.createElement("div");

            container.className =
                "conversation-container";


            const item =
                document.createElement("div");

            item.className =
                "conversation-item";

            item.textContent =
                "Conversation " + conversation.id;


            item.addEventListener("click", () => {

                conversationId =
                    conversation.id;

                loadConversation(
                    conversation.id
                );
            });


            const deleteButton =
                document.createElement("button");

            deleteButton.textContent = "×";

            deleteButton.className =
                "delete-conversation";


            deleteButton.addEventListener(
                "click",
                async (event) => {

                    event.stopPropagation();

                    const confirmed =
                        confirm(
                            "Delete this conversation?"
                        );

                    if (!confirmed) return;


                    const response =
                        await fetch(
                            `${API_URL}/conversation/${conversation.id}`,
                            {
                                method: "DELETE"
                            }
                        );


                    if (response.ok) {

                        if (
                            conversationId ===
                            conversation.id
                        ) {

                            conversationId = null;

                            document.getElementById(
                                "chatBox"
                            ).innerHTML = "";
                        }

                        await loadConversations();
                    }
                }
            );


            container.appendChild(item);

            container.appendChild(
                deleteButton
            );

            conversationList.appendChild(
                container
            );
        });

    } catch (error) {

        console.error(
            "Failed to load conversations:",
            error
        );
    }
}



async function createConversation() {

    try {

        const res =
            await fetch(
                `${API_URL}/conversation`,
                {
                    method: "POST"
                }
            );


        const data =
            await res.json();


        conversationId =
            data.conversation_id;


        console.log(
            "New Conversation ID:",
            conversationId
        );

    } catch (error) {

        console.error(
            "Failed to create conversation:",
            error
        );
    }
}



async function loadConversation(id) {

    try {

        const res =
            await fetch(
                `${API_URL}/conversation/${id}`
            );


        const data =
            await res.json();


        if (!res.ok) {

            console.error(
                "Failed to load conversation:",
                data
            );

            return;
        }


        conversationId = id;


        const chatBox =
            document.getElementById(
                "chatBox"
            );


        chatBox.innerHTML = "";


        data.messages.forEach((message) => {

            const msg =
                document.createElement("div");


            if (
                message.role === "user"
            ) {

                msg.className =
                    "msg user";

                msg.textContent =
                    "You: " +
                    message.content;

            } else {

                msg.className =
                    "msg bot";

                msg.innerHTML =
                    "<strong>Bot:</strong><br>" +
                    marked.parse(
                        message.content
                    );


                msg.querySelectorAll(
                    "pre code"
                ).forEach((block) => {

                    hljs.highlightElement(
                        block
                    );

                });
            }


            chatBox.appendChild(msg);
        });


        chatBox.scrollTop =
            chatBox.scrollHeight;


        await loadConversations();

    } catch (error) {

        console.error(
            "Error loading conversation:",
            error
        );
    }
}



input.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {

            send();
        }
    }
);



async function send() {

    let message =
        input.value.trim();


    if (!message) return;


    if (conversationId === null) {

        await createConversation();


        if (conversationId === null) {

            return;
        }
    }


    const chatBox =
        document.getElementById(
            "chatBox"
        );


    const userMessage =
        document.createElement("div");


    userMessage.className =
        "msg user";


    userMessage.textContent =
        "You: " + message;


    chatBox.appendChild(
        userMessage
    );


    input.value = "";


    const typing =
        document.createElement("div");


    typing.className =
        "msg bot";


    typing.textContent =
        "AI is typing...";


    chatBox.appendChild(
        typing
    );


    sendBtn.disabled = true;


    chatBox.scrollTop =
        chatBox.scrollHeight;


    try {

        const res =
            await fetch(
                `${API_URL}/chat`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        message: message,

                        conversation_id:
                            conversationId

                    })
                }
            );


        const data =
            await res.json();


        if (!res.ok) {

            typing.textContent =
                "Error: " +
                JSON.stringify(data);

            sendBtn.disabled = false;

            return;
        }


        typing.innerHTML =
            "<strong>Bot:</strong><br>" +
            marked.parse(
                data.reply
            );


        typing.querySelectorAll(
            "pre code"
        ).forEach((block) => {

            hljs.highlightElement(
                block
            );

        });


        await loadConversations();


    } catch (error) {

        console.error(
            "Chat error:",
            error
        );


        typing.textContent =
            "Sorry, I'm having trouble connecting to the AI service. Please try again.";
    }


    sendBtn.disabled = false;


    chatBox.scrollTop =
        chatBox.scrollHeight;
}



createConversation().then(() => {

    loadConversations();

});