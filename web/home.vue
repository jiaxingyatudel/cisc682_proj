<style>
#home{
    position: absolute;
    width: 100%;
    height: 100%;
    background-image: url("/web/home_background.jpg");
    background-size: cover;
    background-repeat: no-repeat;
}

#home_title{
    width: 100%;
    text-align: center;
    color: #333;
}

#home_search{
    position: relative;
    margin: 0 auto;
    top: 30%;
    width: 500px;
}
</style>

<template>
    <div id="home">
        <div id="home_search">
            <h1 id="home_title">Tomato Hot Pot</h1>
            <div class="input-group">
                <input type="text" class="form-control" placeholder="">
                <div class="input-group-append">
                    <button class="btn btn-dark" type="button"><i class="fa fa-search" aria-hidden="true"></i></button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
module.exports={}
</script>