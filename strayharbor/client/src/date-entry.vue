<template>
    <div class="date">
        <span class="display-date">{{ display_date }}</span>
    </div>

    <template v-for="upvote_data in upvotes">
        <upvote-entry :upvote_data="upvote_data"></upvote-entry>
    </template>
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
