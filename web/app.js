let user_data={
    user_id:false,
    user_name:false,
    user_email:false,
    register_user_passsword_input_toggle:false,
    register_user_name:"",
    register_user_email:"",
    register_user_password:""
}

let user=new Vue({
    el:"#user",
    data:user_data,
    methods:{
        click_user_register:async function(){
            if(this.register_user_name.length<=0){
                alert("Not valid user name")
                return;
            }
            if(!(/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/.test(this.register_user_email))){
                alert("Not valid email format")
                return;
            }
            if(this.register_user_password.length<=8){
                alert("Password needs to be longer than 8 digits")
                return;
            }

            const response=await fetch("/user_register",{
                method:"POST",
                body:JSON.stringify({
                    user_name: this.register_user_name,
                    user_email: this.register_user_email,
                    user_password: this.register_user_password
                })
            });

            if(response.ok){
                const resp=await response.json();
                this.user_id=resp.user_id;
                this.user_name=resp.user_name;
                this.user_email=resp.user_email;
            }
        },
        click_register_user_passsword_input_toggle:function(){
            this.register_user_passsword_input_toggle=!(this.register_user_passsword_input_toggle)
        }
    }
})