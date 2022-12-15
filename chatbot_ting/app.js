class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        }

        this.state = false;
        this.messages = [];
    }

    display() {
        const {openButton, chatBox, sendButton} = this.args;

        openButton.addEventListener('click', () => this.toggleState(chatBox))

        sendButton.addEventListener('click', () => this.onSendButton(chatBox))

        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({key}) => {
            if (key === "Enter") {
                this.onSendButton(chatBox)
            }
        })
    }

    toggleState(chatbox) {
        this.state = !this.state;

        // show or hides the box
        if(this.state) {
            chatbox.classList.add('chatbox--active')
        } else {
            chatbox.classList.remove('chatbox--active')
        }
    }

    onSendButton(chatbox) {
        var textField = chatbox.querySelector('input');
        let text1 = textField.value
        if (text1 === "") {
            return;
        }

        let msg1 = { name: "User", message: text1}
        this.messages.push(msg1);

        fetch($SCRIPT_ROOT+'/predict', {
            method: 'POST',
            body: JSON.stringify({ 
                message: text1,
                isLogin: localStorage.getItem('token')
            }),
            mode: 'cors',
            headers: {
              'Content-Type': 'application/json'
            },
          })
          .then(r => r.json())
          .then(r => {
            let msg2 = { name: "Sam", message: r.answer, projects: r.projects, researches:r.researches};
            this.messages.push(msg2);
            this.updateChatText(chatbox)
            textField.value = ''

        }).catch((error) => {
            console.error('Error:', error);
            this.updateChatText(chatbox)
            textField.value = ''
          });
    }

    updateChatText(chatbox) {
        var html = '';
        this.messages.slice().reverse().forEach(function(item, index) {
            if (item.name === "Sam")
            {
                if(item.message==="case1")
                {
                    html += '<div class="messages__item messages__item--visitor">'
                    html += 'best projects:<br>'
                    for(let i = 0; i < item.projects.length; i++)
                    {
                        html += `<a href="http://localhost:8080/#/projects/${item.projects[i]["id"]}" target="_blank">${item.projects[i]["project_title"]}</a><br>`
                        html += `Tags: ${item.projects[i]["researches"]}<br>`
                    }
                    html += '</div>'
                }
                else if(item.message==="case2")
                {
                    html += '<div class="messages__item messages__item--visitor">'
                    html += 'all projects:<br>'
                    for(let i = 0; i < item.projects.length; i++)
                    {
                        html += `<a href="http://localhost:8080/#/projects/${item.projects[i]["id"]}" target="_blank">${item.projects[i]["project_title"]}</a><br>`
                        html += `Tags: ${item.projects[i]["researches"]}<br>`
                    }
                    html += '</div>'
                }
                else if(item.message==="case3")
                {
                    html += '<div class="messages__item messages__item--visitor">'
                    html += 'projects about the tags:<br>'
                    for(let i = 0; i < item.projects.length; i++)
                    {
                        html += `<a href="http://localhost:8080/#/projects/${item.projects[i]["id"]}" target="_blank">${item.projects[i]["project_title"]}</a><br>`
                        html += `Tags: ${item.projects[i]["researches"]}<br>`
                    }
                    html += '</div>'
                }
                else if(item.message==="case4")
                {
                    html += '<div class="messages__item messages__item--visitor">'
                    html += 'all researches:<br>'
                    for(let i = 0; i < item.researches.length; i++)
                    {
                        if(i!=0) html += ', '
                        html += `${item.researches[i]}`
                    }
                    html += '</div>'
                }
                else 
                {
                    html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>'
                }  
            }      
            else
            {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>'
            }

          });

        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }
}


const chatbox = new Chatbox();
chatbox.display();