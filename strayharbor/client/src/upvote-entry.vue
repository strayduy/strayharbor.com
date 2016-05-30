<template>
    <div class="like-entry panel panel-default">
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
                    <a class="like-title" :href="upvote_data.url">
                        {{ upvote_data.title }}
                    </a>
                    <div class="bottom-links">
                        <div class="pull-left">
                            <a class="like-comments" :href="upvote_data.permalink">
                                {{ comments_text }}
                            </a>
                        </div>
                        <div class="pull-right text-right">
                            <a class="like-subreddit" v-link="{path: subreddit_url}" :style="{backgroundColor: subreddit_bg_color, color: subreddit_text_color}">
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
