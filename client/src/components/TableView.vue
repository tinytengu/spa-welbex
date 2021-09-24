<template>
  <table class="table">
    <thead v-if="items">
      <tr>
        <th scope="col" v-for="i in fields" :key="i">{{ i }}</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(item, idx) in items" :key="idx">
        <td v-for="field in fields" :key="field">
          {{ item[field] }}
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: 'TableView',
  props: {
    fields: Array,
    items: Array
  }
}
</script>
