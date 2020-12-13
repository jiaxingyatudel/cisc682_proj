<style>
#top_bar{
    position: absolute;
    width: 100%;
    height: 60px;
    border-bottom-color: #333;
    border-bottom-width: 1px;
    border-bottom-style: solid;
    background-color: #eee;
}

#top_bar_search{
    position: absolute;
    top: 10px;
    right: 75px;
    width: 300px;
}

#top_bar_title_container{
    width: 680px;
    margin: auto;
    padding-top: 10px;
    line-height: 40px;
    font-size: 18px;
}
</style>

<template>
    <div id="top_bar">
        <div id="top_bar_title_container"><slot></slot></div>
        <div v-if="top_bar_search" class="input-group" id="top_bar_search">
            <input type="text" class="form-control" placeholder="">
            <div class="input-group-append">
                <button class="btn btn-dark" type="button"><i class="fa fa-search" aria-hidden="true"></i></button>
            </div>
        </div>
    </div>
</template>

<script>
module.exports={
    props:["title","top_bar_search"]
}
</script>