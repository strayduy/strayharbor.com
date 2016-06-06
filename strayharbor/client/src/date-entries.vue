<template>
    <template v-if="$loadingRouteData">
        <div class="text-center">Loading...</div>
    </template>
    <template v-else>
        <template v-for="date_entry in date_entries">
            <div class="row">
                <div class="col-xs-12 col-sm-10 col-sm-offset-1 col-md-8 col-md-offset-2">
                    <date-entry :date="date_entry.date" :posts="date_entry.posts" :upvotes="date_entry.upvotes"></date-entry>
                </div>
            </div>
        </template>

        <template v-if="should_show_pagination">
            <div class="row">
                <div class="col-xs-12 col-sm-10 col-sm-offset-1 col-md-8 col-md-offset-2">
                    <nav>
                        <ul class="pager">
                            <li class="previous disabled" v-show="!has_prev_page">
                                <a>
                                    <span aria-hidden="true">&larr;</span> Newer
                                </a>
                            </li>
                            <li class="previous" v-show="has_prev_page">
                                <a v-link="prev_page">
                                    <span aria-hidden="true">&larr;</span> Newer
                                </a>
                            </li>
                            <li class="next" v-show="has_next_page">
                                <a v-link="next_page">
                                    Older <span aria-hidden="true">&rarr;</span>
                                </a>
                            </li>
                            <li class="next disabled" v-show="!has_next_page">
                                <a>
                                    Older <span aria-hidden="true">&rarr;</span>
                                </a>
                            </li>
                        </ul>
                    </nav>
                </div>
            </div>
        </template>
    </template>
</template>

<script>
import _ from 'lodash';
import DateEntry from './date-entry.vue'

export default {
    components: { DateEntry },
    props: [
        'filter',
    ],
    data: function() {
        return {
            date_entries: [],
            max_pages: 0,
        };
    },
    methods: {
        get_page_obj: function(page) {
            let page_obj = {
                params: {
                    page: page,
                },
            };

            let current_route = this.$route.name;
            if (current_route == 'all' || current_route == 'all_paginated') {
                page_obj.name = 'all_paginated';
            }
            else if (current_route == 'subreddit' || current_route == 'subreddit_paginated') {
                page_obj.name = 'subreddit_paginated';
            }
            else if (current_route == 'posts' || current_route == 'posts_paginated') {
                page_obj.name = 'posts_paginated';
            }

            return page_obj;
        },
    },
    computed: {
        current_page: function() {
            let page = parseInt(this.$route.params.page);
            return _.isNaN(page) ? 1 : page;
        },
        should_show_pagination: function() {
            return this.max_pages > 1;
        },
        has_prev_page: function() {
            return this.current_page > 1;
        },
        has_next_page: function() {
            return this.current_page < this.max_pages;
        },
        prev_page: function() {
            return this.get_page_obj(Math.max(this.current_page - 1, 1));
        },
        next_page: function() {
            return this.get_page_obj(Math.min(this.current_page + 1, this.max_pages));
        },
    },
    route: {
        data: function() {
            let params = this.$route.params;
            let filter = this.filter || {};

            // Pagination
            let page = parseInt(params.page);
            if (page > 1) {
                filter.page = page;
            }

            // Filter by subreddit
            let subreddit = params.subreddit;
            if (subreddit) {
                filter.subreddit = subreddit;
            }

            // Filter by posts
            if (this.$route.name === 'posts' || this.$route.name === 'posts_paginated') {
                filter.only_posts = true;
            }

            // Retrieve a single post
            if (this.$route.name === 'single_post') {
                filter.single_post = `${params.year} ${params.month} ${params.day} ${params.slug}`;
            }

            return this.$http.get('/date-entries.json', filter).then(function success(response) {
                this.date_entries = response.data.date_entries;
                this.max_pages = response.data.max_pages;
            }, function error(response) {
            });
        },
    },
}
</script>
