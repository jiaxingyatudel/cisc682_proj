<style>
</style>

<template>
    <div class="input-group password_input_group">
        <div class="input-group-prepend password_input_group_prepend">
            <span class="input-group-text">{{title}}</span>
        </div>
        <input v-bind:type="(toggle)?('text'):('password')" class="form-control" v-bind:value="value" v-on:input="$emit('input',$event.target.value)">
        <div class="input-group-append">
            <button class="btn btn-outline-secondary" type="button" v-on:click="click_toggle()">
                <span v-if="toggle"><i class="fa fa-eye" aria-hidden="true"></i></span>
                <span v-if="!toggle"><i class="fa fa-eye-slash" aria-hidden="true"></i></span>
            </button>
        </div>
    </div>
</template>

<script>
module.exports={
    props:["title","value"],
    data:function(){
        return{
            toggle:false
        }
    },
    methods:{
        click_toggle:function(){
            this.toggle=!(this.toggle);
        }
    }
}
</script>