<style>
</style>

<template>
    <div class="input-group user_info_input_group">
        <div class="input-group-prepend user_info_input_group_prepend">
            <span class="input-group-text">{{title}}</span>
        </div>
        <input v-if="!toggle" type="text" class="form-control" v-bind:value="old_value" readonly>
        <input v-if="toggle" type="text" class="form-control" v-bind:value="value" v-on:input="$emit('input',$event.target.value)">
        <div v-if="!toggle" class="input-group-append user_info_input_group_append">
            <button class="btn btn-outline-secondary" type="button" v-on:click="click_toggle()">
                <span>Change</span>
            </button>
        </div>
        <div v-if="toggle" class="input-group-append user_info_input_group_append">
            <button class="btn btn-outline-secondary" type="button" v-on:click="click_toggle()">
                <span>Cancel</span>
            </button>
        </div>
        <div v-if="toggle" class="input-group-append user_info_input_group_append">
            <button class="btn btn-dark" type="button" v-on:click="click_toggle();$emit('confirm')">
                <span>Confirm</span>
            </button>
        </div>
    </div>
</template>

<script>
module.exports={
    props:["title","old_value","value"],
    data:function(){
        return{
            toggle:false
        }
    },
    methods:{
        click_toggle:function(){
            this.value=this.old_value;
            this.toggle=!(this.toggle);
        }
    }
}
</script>