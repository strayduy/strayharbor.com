<style>
.date-entry {
    display: block;
    margin-bottom: 60px;
}
.date {
    background-color: #444;
    height: 1px;
    margin: 25px 0 30px 0;
    text-align: center;
}
.display-date {
    background-color: #eeeeee;
    font-size: 25px;
    padding: 0px 10px;
    position: relative;
    top: -20px;
}
</style>

<template>
    <div class="date-entry">
        <div class="date">
            <span class="display-date">{{ display_date }}</span>
        </div>

        <template v-for="upvote_data in upvotes">
            <upvote-entry :upvote_data="upvote_data"></upvote-entry>
        </template>
    </div>
</template>

<script>
import moment from 'moment';
import UpvoteEntry from './upvote-entry.vue'

export default {
    components: { UpvoteEntry },
    props: [
        'date',
        'upvotes',
    ],
    computed: {
        display_date: function() {
            let date = moment(this.date);
            return date.format('MMMM Do, YYYY');
        },
    },
}
</script>
