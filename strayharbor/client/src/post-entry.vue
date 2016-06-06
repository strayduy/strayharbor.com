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
