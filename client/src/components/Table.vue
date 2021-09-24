<template>
  <div class="container">
    <!-- Instruments -->
    <div class="row justify-content-end">
      <div class="col">
        <div class="input-group mb-3">
          <div class="input-group-prepend">
            <!-- Sort by -->
            <div class="dropdown">
              <button class="btn btn-secondary dropdown-toggle" type="button" data-toggle="dropdown">
                Sort by {{ sort.field }}
              </button>
              <div class="dropdown-menu">
                <a class="dropdown-item" href="#" v-for="i in sort.fields" :key="i" @click="sort.field = i">{{ i }}</a>
              </div>
            </div>
            <!-- Sort type -->
            <div class="dropdown">
              <button class="btn btn-secondary dropdown-toggle" type="button" data-toggle="dropdown">
                Sort type {{ sort.type }}
              </button>
              <div class="dropdown-menu">
                <a class="dropdown-item" href="#" v-for="i in sort.types" :key="i" @click="sort.type = i">{{ i }}</a>
              </div>
            </div>
          </div>
          <!-- Sort value -->
          <input type="text" class="form-control" placeholder="" v-model="sort.value">
          <!-- Sort button -->
          <button class="btn btn-primary" @click="fetch_items(true)">Sort</button>
          <!-- Clear button -->
          <button class="btn btn-danger" @click="reset_sort">Clear</button>
        </div>
      </div>
    </div>
    <!-- Table -->
    <div class="row">
      <TableView :fields="table.fields" :items="pageItems"/>
      <Pagination v-if="pagesCount > 1" :perPage="table.perPage" :pages="pagesCount" @pageChanged="table.page = $event"/>
    </div>
  </div>
</template>

<script>
import Pagination from './Pagination'
import TableView from './TableView'

const axios = require('axios')

export default {
  name: 'Table',
  components: { Pagination, TableView },
  data () {
    return {
      items: [],
      table: {
        perPage: 10,
        page: 0,
        fields: [
          'id',
          'name',
          'date',
          'amount',
          'distance'
        ]
      },
      sort: {
        field: '',
        fields: [
          '',
          'Name',
          'Amount',
          'Distance'
        ],
        type: '',
        types: [
          '',
          'Contains',
          'Exact',
          'Bigger',
          'Lower'
        ],
        value: ''
      }
    }
  },
  mounted () {
    this.fetch_items()
  },
  computed: {
    pagesCount () {
      return Math.ceil(this.items.length / this.table.perPage)
    },
    pageItems () {
      if (this.items === undefined || this.items.length === 0) {
        return []
      }

      let start = this.table.page * this.table.perPage
      let end = start + this.table.perPage
      return this.items.slice(start, end)
    }
  },
  methods: {
    fetch_items (sort = false) {
      var _this = this

      let url = 'http://localhost:5000/items'
      if (sort === true) {
        let field = this.sort.field.toLowerCase()
        let type = this.sort.type.toLowerCase()

        url = `http://localhost:5000/items?sort_by=${field}&sort_type=${type}&sort_value=${this.sort.value}`
      }

      axios.get(url)
        .then(function (response) {
          _this.items = response.data
        })
    },
    reset_sort () {
      this.sort.field =
      this.sort.type =
      this.sort.value = ''

      this.fetch_items()
    }
  }
}
</script>
