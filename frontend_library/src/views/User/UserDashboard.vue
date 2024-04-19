<template>
   
  <div>
    <NavBar/>
   <div>
    <h3 style="text-align: center;font-weight: bold;margin-top: 1%;">Welcome, {{ userName }}</h3>
    <input style="width:100%;padding: 0.5%;border-width:0.5cap;border-radius: 10cqb; color:black;font-weight: 700;font-size:large;text-align: center;border-color: black;margin-bottom:2%" type="text" v-model="searchBar" placeholder="Search by book or author">
  </div>
    <div v-for="(section, index) in bookSections" :key="index">
      <div class="section-title-wrapper">
        <h2 class="section-title">{{ section }}</h2>
      </div>
      <button class="scroll-button prev" @click="scrollHorizontal(-1)">
          <i class="bi bi-arrow-left"></i>
        </button>
        <button class="scroll-button next" @click="scrollHorizontal(1)">
          <i class="bi bi-arrow-right"></i>
        </button>
      <div class="row" style="background-color:whitesmoke;">
        <div v-for="book in searchSections(section)" :key="book.id" class="card" style="background-color:whitesmoke;">
          <div class="card-body">
            <button @click="readBook(book.id)" style="border: none;">
            <template v-if="book.coverUrl">
              <img :src="book.coverUrl" loading="lazy" class="card-img-top"
                :class="{ 'disabled-image': book.requested || book.allocated }" alt="Book Cover">
            </template>
            <template v-else>
              <img src="@/assets/default.jpeg" loading="lazy" class="card-img-top" alt="Default Cover">
            </template>
          </button>
            <h6 class="card-subtitle mb-2 text-muted" style="text-align: center;"> by {{ book.authors }}</h6>
            <div class="book-actions text-center">
              <button v-if="book.read === 0 && book.allocated === 0 && !book.requested" type="button"
                class="btn btn-primary mr-2" @click="userRequests(book.id, book.section)">
                Request
              </button>
              <button v-else-if="book.requested && !book.allocated" type="button" class="btn btn-warning" disabled>
                Requested
              </button>
              <button v-else-if="book.allocated && book.read === 0" type="button" class="btn btn-success" disabled>
                Allocated
              </button>
              <button v-else-if="book.read === 1" type="button" class="btn btn-primary" @click="userRequests(book.id, book.section)">
                Request
              </button>
            </div>
          </div>
        </div>
      </div>
    
    </div>
  </div>

</template>

<script>
import NavBar from "../../components/NavBar.vue";

import axios from "axios";

export default {
  data() {
    return {
      userName: "",
      books: [],
      searchBar: "",
    };
  },
  name: "UserDashboard",
  components: {
    NavBar,
  },
  computed: {
    bookSections() {
      return Array.from(new Set(this.books.map(book => book.section)));
    }
  },
  methods: {
    async getBookList() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/books", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        });
        this.books = response.data;
        await this.setUsersLastVisitTime();
        await this.fetchBookCovers();
      } catch (error) {
        console.error("Error fetching books:", error);
      }
    },
    readBook(book_id) {
      this.$router.push({ name: 'BookPage', params: { id: book_id} });
    },
    searchSections(section) {
      return this.books.filter(book => {
        const sectionMatch = book.section === section;
        const searchMatch = 
          book.name.toLowerCase().includes(this.searchBar.toLowerCase()) ||
          book.authors.toLowerCase().includes(this.searchBar.toLowerCase());
        return sectionMatch && (this.searchBar === "" || searchMatch);
      });
    },
    async fetchBookCovers() {
      for (const book of this.books) {
        try {
          const coverUrl = await this.getBookCover(book);
          book.coverUrl = coverUrl;
        } catch (error) {
          console.error("Error fetching book cover:", error);
          book.coverUrl = null; 
        }
      }
    },
    getBookCover(book) {
      const apiUrl = `http://localhost:5000/bookcover?book_title=${encodeURIComponent(book.name)}
      &author_name=${encodeURIComponent(book.authors)}
      &isbn=${encodeURIComponent(book.isbn)}`;

      return axios
        .get(apiUrl)
        .then((response) => {
          console.log(response.data);
          return response.data;
        })
        .catch((error) => {
          console.error("Error fetching book cover:", error);
          return null;
        });
    },
    userRequests(bookId, sectionName) {
      console.log(bookId, sectionName);
      const requestData = {
        book_id: bookId,
      };
      axios
        .post("http://127.0.0.1:5000/api/request/book", requestData, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        })
        .then((response) => {
          console.log(response.data);
          console.log("Request sent");
          this.getBookList();
        })
        .catch((error) => {
          alert(error.response.data.error);
          console.log(error);
        });
    },
    async setUsersLastVisitTime(){
      const response = await axios.post("http://127.0.0.1:5000/api/track-last-login" ,{}, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
        }
      })
      if (response.status === 200) {
        console.log("Last login time updated: ", response.data);
      } else {
        console.error("Failed to update last login time: ", response.data.error);
      }
    },
    scrollHorizontal(direction) {
        const scrollContainer = document.querySelector(".row");
        const scrollAmount = 300 * direction;
        scrollContainer.scrollBy({
          left: scrollAmount,
          behavior: "smooth"
        });
      }
  },
  mounted() {
    this.userName = JSON.parse(localStorage.getItem("user"));
    this.getBookList();
  },
};
</script>

<style scoped>

.section-title {
  background-color: #222;
  color:white;
  text-align: center;
}

.book-cover {
  height:150px;
  align-items: start;
  object-fit: contain;
  margin-bottom: 0.25rem;
}

.book-cover.disabled-image {
  opacity: 0.5;
}

.book-actions {
  display: flex;
  gap: 10px;
  justify-content: center;
}

.btn {
  color: white;
  border: none;
  justify-content: center;
}

.btn:hover {
  background-color: rgba(72, 255, 72, 0.9);
}

.btn-warning {
  background-color: rgba(255, 221, 0, 0.719);
  color: black;
  pointer-events: none;
  cursor: not-allowed;
  opacity: 0.5;
}

.btn-warning:hover {
  background-color: rgba(255, 221, 0, 0.9);
}

.btn-primary {
  background-color: rgba(0, 123, 255, 0.719);
}

.btn-primary:hover {
  background-color: rgba(0, 123, 255, 0.9);
}

.row {
  margin-left:0.75%;
  align-items: stretch;
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  overflow-x: auto;
  overflow-y: hidden;
}

.card {
  max-width: 13.333%;
  padding: .75rem;
  margin-bottom: 2rem;
  border: 0;
  flex-basis: 33.333%;
  flex-grow: 0;
  flex-shrink: 0;
}

.card-img-top {
  margin-bottom: .75rem;
  width: 100%;
  height: 300px;
}

.card-text {
  font-size: 85%;
}

::-webkit-scrollbar {
  width: 12px;
  height: 12px;
}

::-webkit-scrollbar-button {
  width: 0;
  height: 0;
}

::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.5);
  border-radius: 6px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.6);
}

::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 6px;
}

.scroll-button {
      position: absolute;
      top: 60%;
      transform: translateY(-50%);
      background: transparent;
      cursor: pointer;
      padding: 5px;
      font-size: 1.5em;
      color: white;
      background-color: #007bff;
  }
  
  .scroll-button.prev {
      left: 2;
  }
  
  .scroll-button.next {
      right: 0;
  }
</style>
