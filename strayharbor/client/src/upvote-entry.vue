<style>
.upvote-entry {
    margin-bottom: 40px;
}
.upvote-title {
    display: block;
    font-size: 22px;
    padding-bottom: 45px;
}
.upvote-title:hover,
.upvote-title:active {
    text-decoration: none;
}
.media,
.media-body {
    overflow: visible;
}
.media-body {
    position: relative;
}
.upvote-comments,
.upvote-comments:hover,
.upvote-comments:focus,
.upvote-comments:active {
    color: #888;
}
.upvote-subreddit {
    border-radius: 4px;
    padding: 3px 6px;
}
.upvote-subreddit,
.upvote-subreddit:hover,
.upvote-subreddit:focus,
.upvote-subreddit:active {
    color: #fff;
}
.bottom-links {
    bottom: -5px;
    position: absolute;
    width: 100%;
}
</style>

<template>
    <div class="upvote-entry panel panel-default">
        <div class="panel-body">
            <div class="media">
                <template v-if="has_thumbnail">
                    <div class="media-left">
                        <a :href="upvote_data.url">
                            <img :src="upvote_data.thumbnail">
                        </a>
                    </div>
                </template>
                <div class="media-body">
                    <a class="upvote-title" :href="upvote_data.url">
                        {{ upvote_data.title }}
                    </a>
                    <div class="bottom-links">
                        <div class="pull-left">
                            <a class="upvote-comments" :href="comments_url">
                                {{ comments_text }}
                            </a>
                        </div>
                        <div class="pull-right text-right">
                            <a class="upvote-subreddit" v-link="{path: subreddit_url}" :style="{backgroundColor: subreddit_bg_color, color: subreddit_text_color}">
                                {{ subreddit_text }}
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import randomColor from 'randomcolor';

// http://stackoverflow.com/a/11868398
function getContrastYIQ(hexcolor) {
    let r = parseInt(hexcolor.substr(0,2),16);
    let g = parseInt(hexcolor.substr(2,2),16);
    let b = parseInt(hexcolor.substr(4,2),16);
    let yiq = ((r*299)+(g*587)+(b*114))/1000;
    return (yiq >= 128) ? '#333' : '#fff';
}

export default {
    props: [
        'upvote_data',
    ],
    computed: {
        has_thumbnail: function() {
            let thumbnail = this.upvote_data.thumbnail;
            return thumbnail && thumbnail !== 'self' && thumbnail !== 'default';
        },
        comments_text: function() {
            return this.upvote_data.num_comments + ' comments';
        },
        comments_url: function() {
            return 'https://www.reddit.com' + this.upvote_data.permalink;
        },
        subreddit_text: function() {
            return '/r/' + this.upvote_data.subreddit;
        },
        subreddit_url: function() {
            return '/r/' + this.upvote_data.subreddit;
        },
        subreddit_bg_color: function() {
            return randomColor({seed: this.upvote_data.subreddit});
        },
        subreddit_text_color: function() {
            let bg_color = this.subreddit_bg_color;
            let contrast_color = getContrastYIQ(bg_color.slice(1));
            return contrast_color;
        },
    },
}
</script>
