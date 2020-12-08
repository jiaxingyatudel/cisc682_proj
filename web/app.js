const store=new Vuex.Store({
    state:{
        user_id:false,
        user_checked:false
    },
    mutations:{
        user_check(state,user_id){
            state.user_id=user_id;
            state.user_checked=true;
        }
    }
});

const routes=[
    {
        path:"/",
        component:httpVueLoader("/web/home.vue")
    },
    {
        path:"/home",
        component:httpVueLoader("/web/home.vue")
    },
    {
        path:"/following_users",
        component:httpVueLoader("/web/following_users.vue"),
        beforeEnter:function(to,from,next){
            if((store.state.user_checked)&&(!store.state.user_id)){
                next({path:"/"});
            }else{
                next();
            }
        }
    },
    {
        path:"/compose",
        component:httpVueLoader("/web/compose.vue"),
        beforeEnter:function(to,from,next){
            if((store.state.user_checked)&&(!store.state.user_id)){
                next({path:"/"});
            }else{
                next();
            }
        }
    }
];

(async function(){
    const response=await fetch("/check_user_cookie",{
        method:"POST",
        credentials:"include"
    });
    if(response.ok){
        const resp=await response.json();
        if(!resp.err){
            store.commit("user_check",resp.user_id);
        }else{
            store.commit("user_check",false);
        }

        const router=new VueRouter({
            routes:routes
        });

        new Vue({
            el:"#app",
            router:router,
            components:{
                "nav_menu":httpVueLoader("/web/menu.vue"),
                "user":httpVueLoader("/web/user.vue")
            }
        });
    }
})();