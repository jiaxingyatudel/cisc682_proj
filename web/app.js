let hash={
    current_hash:window.location.hash
}

window.addEventListener("hashchange",()=>{
    hash.current_hash=window.location.hash
},false);

const routes={
    "":"HOME",
    "#home":"HOME",
    "#my":"MY",
    "#like":"LIKE"
};

let user_data={
    user_id:false,
    user_name:false,
    user_email:false,
    user_login_register_toogle:false,
    register_user_passsword_input_toggle:false,
    register_user_name:"",
    register_user_email:"",
    register_user_password:"",
    login_user_email:"",
    login_user_password:"",
    login_user_passsword_input_toggle:false,
    user_info_input_user_name:"",
    user_info_input_user_email:"",
    user_info_user_name_input_toggle:false,
    user_info_user_email_input_toggle:false
}

let router=new Vue({
    el:"#router",
    data:hash,
    computed:{
        component:function(){
            if(!(this.current_hash in routes)){
                return "HOME";
            }else{
                return routes[this.current_hash];
            }
        }
    }
});

let home=new Vue({
    el:"#home",
    data:{}
});

let menu=new Vue({
    el:"#menu",
    data:user_data,
    methods:{}
});

let compose=new Vue({
    el:"#compose",
    data:user_data,
    methods:{}
});

let user=new Vue({
    el:"#user",
    data:user_data,
    mounted:async function(){
        const response=await fetch("/check_user_cookie",{
            method:"POST",
            credentials:"include"
        });
        if(response.ok){
            const resp=await response.json();
            if(!resp.err){
                this.user_id=resp.user_id;
                this.user_name=resp.user_name;
                this.user_email=resp.user_email;
            }
        }
    },
    methods:{
        click_register_btn:function(){
            this.user_login_register_toogle=false;
            $("#user_modal").modal("show");
        },
        click_login_btn:function(){
            this.user_login_register_toogle=true;
            $("#user_modal").modal("show");
        },
        click_user_btn:function(){
            $("#user_modal").modal("show");
        },
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
                    user_name:this.register_user_name,
                    user_email:this.register_user_email,
                    user_password:this.register_user_password
                })
            });
            if(response.ok){
                const resp=await response.json();
                if(!resp.err){
                    this.user_id=resp.user_id;
                    this.user_name=resp.user_name;
                    this.user_email=resp.user_email;
                    this.register_user_name="";
                    this.register_user_email="";
                    this.register_user_password="";
                    this.login_user_email="";
                    this.login_user_password="";
                    $("#user_modal").modal("hide");
                }
                if(resp.err==1){
                    alert("Email already registered");
                }
            }
        },
        click_user_login:async function(){
            const response=await fetch("/user_login",{
                method:"POST",
                body:JSON.stringify({
                    user_email:this.login_user_email,
                    user_password:this.login_user_password
                })
            });
            if(response.ok){
                const resp=await response.json();
                if(!resp.err){
                    this.user_id=resp.user_id;
                    this.user_name=resp.user_name;
                    this.user_email=resp.user_email;
                    this.register_user_name="";
                    this.register_user_email="";
                    this.register_user_password="";
                    this.login_user_email="";
                    this.login_user_password="";
                    $("#user_modal").modal("hide");
                }
                if(resp.err==1){
                    alert("Email and password not match");
                }
            }
        },
        click_user_logout:async function(){
            const response=await fetch("/user_logout",{
                method:"POST",
                credentials:"include"
            });
            if(response.ok){
                const resp=await response.json();
                if(!resp.err){
                    this.user_id=false;
                    this.user_name=false;
                    this.user_email=false;
                    this.register_user_name="";
                    this.register_user_email="";
                    this.register_user_password="";
                    this.login_user_email="";
                    this.login_user_password="";
                    window.location.reload();
                }
            }
        },
        click_user_logout_all:async function(){
            const response=await fetch("/user_logout_all",{
                method:"POST",
                credentials:"include",
                body:JSON.stringify({
                    user_id:this.user_id,
                })
            });
            if(response.ok){
                const resp=await response.json();
                if(!resp.err){
                    this.user_id=false;
                    this.user_name=false;
                    this.user_email=false;
                    this.register_user_name="";
                    this.register_user_email="";
                    this.register_user_password="";
                    this.login_user_email="";
                    this.login_user_password="";
                    window.location.reload();
                }
            }
        },
        click_user_login_register_toogle:function(b){
            this.user_login_register_toogle=b;
        },
        click_register_user_passsword_input_toggle:function(){
            this.register_user_passsword_input_toggle=!(this.register_user_passsword_input_toggle);
        },
        click_login_user_passsword_input_toggle:function(){
            this.login_user_passsword_input_toggle=!(this.login_user_passsword_input_toggle);
        },
        click_user_info_user_name_input_toggle:function(){
            this.user_info_user_name_input_toggle=!(this.user_info_user_name_input_toggle);
            this.user_info_input_user_name=this.user_name;
        },
        click_user_info_user_email_input_toggle:function(){
            this.user_info_user_email_input_toggle=!(this.user_info_user_email_input_toggle);
            this.user_info_input_user_email=this.user_email;
        },
        click_user_info_user_name_confirm:async function(){
            let b=confirm("Are you sure to change your name to "+this.user_info_input_user_name);
            if(!b){
                return;
            }else{
                const response=await fetch("/user_change_user_name",{
                    method:"POST",
                    credentials:"include",
                    body:JSON.stringify({
                        user_id:this.user_id,
                        user_name:this.user_info_input_user_name
                    })
                });
                if(response.ok){
                    const resp=await response.json();
                    if(!resp.err){
                        this.user_name=resp.user_name;
                    }
                    if(resp.err==1){
                        alert("System error");
                    }
                }
                this.user_info_user_name_input_toggle=false;
                this.user_info_input_user_name=this.user_name;
            }
        },
        click_user_info_user_email_confirm:async function(){
            let b=confirm("Are you sure to change your email to "+this.user_info_input_user_email);
            if(!b){
                return;
            }else{
                const response=await fetch("/user_change_user_email",{
                    method:"POST",
                    credentials:"include",
                    body:JSON.stringify({
                        user_id:this.user_id,
                        user_email:this.user_info_input_user_email
                    })
                });
                if(response.ok){
                    const resp=await response.json();
                    if(!resp.err){
                        this.user_email=resp.user_email;
                    }
                    if(resp.err==1){
                        alert("System error");
                    }
                    if(resp.err==2){
                        alert("Email already registered");
                    }
                }
                this.user_info_user_email_input_toggle=false;
                this.user_info_input_user_email=this.user_email;
            }
        }
    }
});