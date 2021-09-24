<template>
  <div class="container">
    <!-- Instruments -->
    <div class="row justify-content-end">
      <div class="col">
        <div class="input-group mb-3">
          <div class="input-group-prepend" id="button-addon3">
            <!-- Sort by -->
            <div class="dropdown">
              <button class="btn btn-secondary dropdown-toggle" type="button" id="sortByBtn" data-toggle="dropdown">
                Sort by {{ sort_field }}
              </button>
              <div class="dropdown-menu" aria-labelledby="sortByBtn">
                <a class="dropdown-item" href="#" v-for="i in sort_fields" :key="i" @click="sort_field = i">{{ i }}</a>
              </div>
            </div>
            <!-- Sort type -->
            <div class="dropdown">
              <button class="btn btn-secondary dropdown-toggle" type="button" id="sortTypeBtn" data-toggle="dropdown">
                Sort type {{ sort_type }}
              </button>
              <div class="dropdown-menu" aria-labelledby="sortTypeBtn">
                <a class="dropdown-item" href="#" v-for="i in sort_types" :key="i" @click="sort_type = i">{{ i }}</a>
              </div>
            </div>
          </div>
          <!-- Sort value -->
          <input type="text" class="form-control" placeholder="" v-model="sort_value">
          <!-- Sort button -->
          <button class="btn btn-primary" @click="fetch_items(true)">Sort</button>
          <!-- Clear button -->
          <button class="btn btn-danger" @click="reset_sort">Clear</button>
        </div>
      </div>
    </div>
    <!-- Table -->
    <div class="row">
      <table class="table">
        <thead v-if="items">
          <tr>
            <th scope="col" v-for="i in table_fields" :key="i">{{ i }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="i in get_items()" :key="i.id">
            <td v-for="f in table_fields" :key="f">
              {{ i[f] }}
            </td>
          </tr>
        </tbody>
      </table>
      <Pagination v-if="pagesCount > 1" :perPage="table.perPage" :pages="pagesCount" @pageChanged="table.page = $event"/>
    </div>
  </div>
</template>

<script>
import Pagination from './Pagination'

const axios = require('axios')

export default {
  components: { Pagination },
  name: 'Table',
  data () {
    return {
      items: [],
      table: {
        perPage: 10,
        page: 0
      },
      sort_field: null,
      sort_fields: [
        '',
        'Name',
        'Amount',
        'Distance'
      ],
      sort_type: null,
      sort_types: [
        '',
        'Contains',
        'Exact',
        'Bigger',
        'Lower'
      ],
      sort_value: '',
      table_fields: [
        'id',
        'name',
        'date',
        'amount',
        'distance'
      ]
    }
  },
  mounted () {
    this.sort_field = this.sort_fields[0]
    this.sort_type = this.sort_types[0]

    this.fetch_items()
  },
  computed: {
    pagesCount () {
      return Math.ceil(this.items.length / this.table.perPage)
    }
  },
  methods: {
    fetch_items (sort = false) {
      var _this = this

      let url = 'http://localhost:5000/items'
      if (sort === true) {
        let field = this.sort_field.toLowerCase()
        let type = this.sort_type.toLowerCase()

        url = `http://localhost:5000/items?sort_by=${field}&sort_type=${type}&sort_value=${this.sort_value}`
      }

      axios.get(url)
        .then(function (response) {
          _this.items = response.data
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    reset_sort () {
      this.sort_field =
      this.sort_type =
      this.sort_value = ''

      this.fetch_items()
    },
    get_items () {
      let start = this.table.page * this.table.perPage
      let end = start + this.table.perPage
      return this.items.slice(start, end)
    }
  }
}
</script>
