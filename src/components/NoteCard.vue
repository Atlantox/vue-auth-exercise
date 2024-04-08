<script setup>
import { defineProps } from 'vue'

const props = defineProps({
    id: {type: Number},
    title:{ type: String },
    content:{ type: String },
    created:{ type: String }
})
</script>

<template>
    <article>
        <h5>{{ props.title }}</h5>
        <p> {{ props.content }}</p>
        <span> {{ props.created }}</span>
        <div>
            <a :href="'/noteForm/' + props.id">
                <button>Ver</button>
            </a>
        </div>
        <div>
            <a href="">
                <button>Borrar</button>
            </a>
        </div>
    </article>
</template>

<style scoped>
    h5, p, span{
        width:100%;
    }

    article{
        width:25%;
        border:2px grey solid;
    }
</style>