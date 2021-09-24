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
      <nav v-if="get_pages_count() != 0">
        <ul class="pagination">
          <!-- Previous -->
          <li class="page-item" :class="page == 0 ? 'disabled' : ''">
            <a class="page-link" href="#" @click.prevent="page--">Previous</a>
          </li>
          <!-- Pages -->
          <li class="page-item" :class="page == i - 1 ? 'active' : ''" v-for="i in get_pages_count()" :key="i">
            <a class="page-link" href="#" @click.prevent="page = i - 1">{{ i }}</a>
          </li>
          <!-- Next -->
          <li class="page-item" :class="page == get_pages_count() - 1 ? 'disabled' : ''">
            <a class="page-link" href="#" @click.prevent="page++">Next</a>
          </li>
        </ul>
      </nav>
    </div>
  </div>
</template>

<script>
const axios = require('axios')

export default {
  name: 'Table',
  data () {
    return {
      items: [],
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
      ],
      page: 0,
      perPage: 10
    }
  },
  mounted () {
    this.sort_field = this.sort_fields[0]
    this.sort_type = this.sort_types[0]

    this.fetch_items()
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
    get_pages_count () {
      return Math.ceil(this.items.length / this.perPage)
    },
    get_items () {
      let start = this.page * this.perPage
      let end = start + this.perPage
      return this.items.slice(start, end)
    }
  }
}
</script>
