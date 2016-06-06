<style>
    .post-entry {
        margin-bottom: 40px;
    }
    .post-entry .panel-body {
        padding: 25px 25px 10px 25px;
    }
    .post-title {
        margin: 5px 0 20px 0;
    }
    .post-content {
        margin-bottom: 25px;
    }
    .posts-link {
        border: 1px solid #337ab7;
        border-radius: 4px;
        margin-right: -10px;
        padding: 2px 5px;
    }
    .posts-link:focus,
    .posts-link:hover {
        border: 1px solid #23527c;
    }
</style>

<template>
    <div class="post-entry panel panel-default">
        <div class="panel-body">
            <h3 class="post-title">
                <a :href="post_data.url">
                    {{ post_data.title }}
                </a>
            </h3>
            <div class="post-content">
                {{{ post_data.content }}}
            </div>
            <div class="text-right">
                <a class="posts-link" href="/posts">
                    self.posts
                </a>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: [
        'post_data',
    ],
    computed: {
        url: function() {
        },
    },
}
</script>
