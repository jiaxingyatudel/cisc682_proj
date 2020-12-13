<style>
.compose_input_group{
    margin-bottom: 10px;
}

.compose_input_group_prepend>span{
    min-width: 140px;
}

#compose_tag_container{
    margin-bottom: 10px;
}
</style>

<template>
    <div>
        <div class="content_container">
            <div class="content">
                <div class="card">
                    <div class="card-body">
                        <div class="input-group compose_input_group">
                            <div class="input-group-prepend compose_input_group_prepend">
                                <span class="input-group-text">Title</span>
                            </div>
                            <input type="text" class="form-control" v-model="title_input">
                        </div>
                        <label>Add categories to your recipe makes others easier to find it</label>
                        <div class="input-group compose_input_group">
                            <div class="input-group-prepend compose_input_group_prepend">
                                <span class="input-group-text">Categories</span>
                            </div>
                            <input type="text" class="form-control" v-model="new_tag_input">
                            <div class="input-group-append">
                                <button class="btn btn-outline-secondary" type="button"><i class="fa fa-plus" aria-hidden="true"></i></button>
                            </div>
                        </div>
                        <div id="compose_tag_container">
                            <i class="fa fa-tags" aria-hidden="true"></i>&nbsp;(Your recipe has no categories now)
                        </div>
                        <div class="input-group compose_input_group">
                            <textarea style="height:400px;resize:none" class="form-control" placeholder="Write you recipe here" v-model="title_input"></textarea>
                        </div>
                        <div>
                            <div class="btn-group" style="float:right;">
                                <button type="button" class="btn btn-dark">Publish</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <top-bar v-bind:top_bar_search="false"><span>Compose Recipe</span></top-bar>
    </div>
</template>

<script>
module.exports={
    data:function(){
        return{
            title_input:"",
            new_tag_input:"",
            text_input:"",
        }
    },
    components:{
        "top-bar":httpVueLoader("/web/top_bar.vue")
    }
}
</script>