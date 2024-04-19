<template>
  <div>
  <NavBar />

  <h2 style="text-align: center;margin-top:2.5%">Available Books</h2>

  <div class="search-section">
    <input style="width:100%;padding: 0.5%;border-width:0.5cap;border-radius: 10cqb; color:black;font-weight: 700;font-size:large;text-align: center;border-color: black;" type="text" v-model="searchBar" placeholder="Search by book or author">
  </div>


  <div v-if="searchBooks.length > 0">
    <table class="table">
      <thead>
        <tr>
          <th>Book Name</th>
          <th>Author</th>
          <th>Section</th>
          <th>ISBN</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="book in searchBooks" :key="book.book_id">
          <td>{{ book.book_name }}</td>
          <td>{{ book.authors }}</td>
          <td>{{ book.section_name }}</td>
          <td>{{ book.isbn }}</td>

        </tr>
      </tbody>
    </table>
  </div>
  <div v-else>
    <p>Not found</p>
  </div>

</div>

</template>

<script>
import axios from "axios";
import NavBar from "../../components/NavBar.vue";
export default {
  name: "StatusBooks",
  components: {
    NavBar,
  },
  data() {
    return {
      books: [],
      searchBar: '', 
    };
  },
  methods: {
    async bookslist() {
  try {
    const headers = {
      Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
    };

    const response = await axios.get(
      "http://127.0.0.1:5000/api/fetch/librarian/books",
      { headers }
    );

    this.books = response.data;
    console.log(this.books);
  } catch (error) {
    console.log(error);
  }
},

  },
  computed: {
    searchBooks() {
      return this.books.filter(book =>
        book.book_name.toLowerCase().includes(this.searchBar.toLowerCase()) ||
        book.authors.toLowerCase().includes(this.searchBar.toLowerCase()) ||
        book.section_name.toLowerCase().includes(this.searchBar.toLowerCase()) ||
        book.isbn.toLowerCase().includes(this.searchBar.toLowerCase())

      );
    }
  },
  created() {
    this.bookslist();
  },
};
</script>
<style scoped>
.btn {

  justify-content: space-around;
  align-items: center;
  padding: 5%;
  margin: 2%;
}


*,
*:before,
*:after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}


table {
  width: 90%;
  background: #333;
  border-radius: 0.25em;
  border-collapse: collapse;
  margin-left:5%;
  margin-top: 2%;
}

th {
  border-bottom: 1px solid #364043;
  color: #E2B842;
  font-size:large;
  font-weight: 600;
  padding: 0.3em 1em;
  text-align: left;
}

td {
  color: #fff;
  font-weight: 400;
  padding: 0.65em;
  text-align: left;
}

.disabled td {
  color: #4F5F64;
}

tbody tr {
  transition: background 0.25s ease;
}

tbody tr:hover {
  background: #014055;
}
</style>
