css = '''
<style>

@media (min-width: calc(54rem)) {
    .st-emotion-cache-1ibsh2c {
         padding-left: 0rem; 
        padding-right: 0rem; 
    }
}


.stMainBlockContainer{
width: 63%;
}


.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
        width: 80%;
    float: right;
    padding: 0px 0.5rem;
    margin-top: 1.7rem;
}
}
.chat-message.bot {
    background-color: #475063;
    width: 80%;
    float: left;
}
}



.chat-message{

}

.message_user{
padding: 0.5rem;

}

.message_bot{
padding: 1.5rem;
}

.bot{
width: 93%;
    padding: 0 1.5rem;
    color: #fff;
    justify-items: left;
    align-content: center;
    }

.user{width: 93%;
    padding: 0 1.5rem;
    color: #fff;
    justify-items: right;
    display: flex;
    justify-content: flex-end;
    align-content: center;
}

.avatar_user{
max-width: 2rem;
  max-height: 2rem;
  object-fit: cover; 
  margin-top: 0.5rem;
}



.avatar_bot{
max-width: 2rem;
  max-height: 2rem;
  object-fit: cover; 
  margin-top: 22px;
  
}



@media (max-width: 768px) {
    .stMainBlockContainer {
        width: 94%;  /* Apply 94% width only on mobile devices */
    }
}


</style>



'''





user_template = '''
<div class="chat-message user">
    <div class="message_user">{{MSG}}</div>
    <div class="avatar_user">
        <img src="https://i.ibb.co/kQ7m5W9/user-image.png">
    </div>    
</div>
'''


bot_template = '''
<div class="chat-message bot">
    <div class="avatar_bot">
        <img src="https://i.ibb.co/d55q7cM/bot-png.png">
    </div>
    <div class="message_bot">{{MSG}}</div>
</div>
'''



