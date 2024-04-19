<template>
  <div>
    <NavBar/>

    <h2 style="text-align: center;margin-top:2.5%">You have returned these books:</h2>
    <input style="width:100%;padding: 0.5%;border-width:0.5cap;border-radius: 10cqb; color:black;font-weight: 700;font-size:large;text-align: center;border-color: black;margin-bottom:2%" type="text" v-model="searchBar" placeholder="Search by book or author or section">

            <div v-if="listreturned.length > 0">
              <table class="table center-table">
                <thead>
                  <tr>
                    <th>Book Name</th>
                    <th>Author</th>
                    <th>Section</th>
                    <th>Feedback Given</th>
                    <th>Rating Given</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="book in filteredReturnedBooks" :key="book.book_id">
                    <td>{{ book.book_title }}</td>
                    <td>{{ book.author }}</td>
                    <td>{{ book.section }}</td>
                    <td>{{ book.feedback }}</td>
                    <td><span v-for="i in book.rating" :key="i">⭐</span></td>
                  </tr>
                </tbody>
              </table>
    
            </div>
            <div v-else>
              <p>Not found</p>
            </div>
          </div>
  
  <FootBar/>
</template>

<script>
import axios from "axios";
import NavBar from "@/components/NavBar.vue";

export default {
  name: "UserHistory",
  data() {
    return {
      listreturned: [],
      rating: null,
      comments: "",
      searchBar: "",
    };
  },
  components:{
    NavBar,
  },
  computed: {
    filteredReturnedBooks() {
      return this.listreturned.filter(book =>
        book.book_title.toLowerCase().includes(this.searchBar.toLowerCase()) ||
        book.author.toLowerCase().includes(this.searchBar.toLowerCase()) ||
        book.section.toLowerCase().includes(this.searchBar.toLowerCase())
      );
    }
  },
  methods: {
    async fetchlistreturned() {
      try {
        const response = await axios.get(
          "http://127.0.0.1:5000/api/fetch_returned_books",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        if (response.status === 200) {
          this.listreturned = response.data;
        } else {
          console.error("Failed to fetch returned books");
        }
      } catch (error) {
        console.error("Error fetching returned books:", error);
      }
    },
    
  },
  mounted() {
    this.fetchlistreturned();
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
  text-align: center;
}

td {
  color: #fff;
  font-weight: 400;
  padding: 0.65em;
  text-align: center;
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