css = '''
<style>

@media (min-width: calc(54rem)) {
    .st-emotion-cache-1ibsh2c {
         padding-left: 0rem; 
        padding-right: 0rem; 
    }
}


.stMainBlockContainer{
width: 65%;
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

.bot{width: 93%;
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
.avatar img {
  max-width: 30px;
  max-height: 30px;
  border-radius: 50%;
  object-fit: cover; 
}









'''



bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://www.pngwing.com/en/free-png-dkjwv/" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message_bot">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="message_user">{{MSG}}</div>
    <div class="avatar">
        <img src="https://i.ibb.co/rdZC7LZ/Photo-logo-1.png">
    </div>    
</div>
'''
