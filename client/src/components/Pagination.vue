<template>
  <nav>
    <ul class="pagination">
      <!-- Previous -->
      <li class="page-item" :class="page == 0 ? 'disabled' : ''">
        <a class="page-link" href="#" @click.prevent="page--">Previous</a>
      </li>
      <!-- Pages -->
      <li class="page-item" :class="page == i - 1 ? 'active' : ''" v-for="i in pages" :key="i">
        <a class="page-link" href="#" @click.prevent="page = i - 1">{{ i }}</a>
      </li>
      <!-- Next -->
      <li class="page-item" :class="page == pages - 1 ? 'disabled' : ''">
        <a class="page-link" href="#" @click.prevent="page++">Next</a>
      </li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: 'Pagination',
  props: {
    // Total pages count
    pages: Number
  },
  data () {
    return {
      // Current page
      page: 0
    }
  },
  watch: {
    /**
     * Emit pageChanged event when 'page' value changed
     */
    page (newValue, oldValue) {
      this.$emit('pageChanged', newValue)
    }
  }
}
</script>
