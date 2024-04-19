<template>
  <div>
    <NavBar />
    <h3 style="text-align: center;font-weight: bold;margin-top: 2%;">Your Books</h3>

    <div v-if="myBooks.length > 0">
      <div class="row">
        <div v-for="book in myBooks" :key="book.book_id" class="card" style="background-color: whitesmoke;">
          <div class="card-body">
            <template v-if="book.coverUrl">
              <img :src="book.coverUrl" class="card-img-top" alt="Book Cover">
            </template>
            <template v-else>
              <img src="@/assets/default.jpeg" class="card-img-top" alt="Default Cover">
            </template>
            <h6 class="card-subtitle mb-2 text-muted" style="text-align: center;"> by {{ book.authors }}</h6>
            <div class="book-actions d-flex text-center" style="justify-content: center;">
              <button type="button" class="btn btn-primary mr-2" @click="readBook(book.book_id)">
                Read
              </button>
              <button type="button" class="btn btn-warning" @click="returnBook(book.book_id, book.user_id)">
                Return
              </button>

            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from "../../components/NavBar.vue"; // Make sure to adjust the path if necessary
import axios from "axios";

export default {
  data() {
    return {
      myBooks: [],
      rating: null,
      comments: "",
      searchQuery: "",
    };
  },

  methods: {
    readBook(book_id) {
      this.$router.push({ name: 'BookPage', params: { id: book_id} });
    },
    searchBooks() {
      return this.myBooks.filter(book => {
        const searchMatch =
          (book.name && book.name.toLowerCase().includes(this.searchQuery.toLowerCase())) ||
          (book.authors && book.authors.toLowerCase().includes(this.searchQuery.toLowerCase()));
        return (this.searchQuery === "" || searchMatch);
      });
    }
    ,
    async fetchIssuedBooks() {
      try {
        const response = await axios.get(
          "http://127.0.0.1:5000/api/fetch_my_books",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`
            }
          }
        );
        if (response.status === 200) {
          this.myBooks = response.data;
          await this.fetchBookCovers();
        } else {
          console.error("Failed to fetch my books");
        }
      } catch (error) {
        console.error("Error fetching my books:", error);
      }
    },
    async fetchBookCovers() {
      for (const book of this.myBooks) {
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
    async returnBook(book_id, user_id) {
      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/api/return/book",
          {
            book_id: book_id,
            user_id: user_id
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`
            }
          }
        );
        if (response.status === 200) {
          console.log("Book returned successfully");
          this.fetchIssuedBooks();
        } else {
          console.error("Failed to return the book");
        }
      } catch (error) {
        console.error("Error returning the book:", error);
      }
    },
 
    calculateDaysLeft(returnDate) {
      const returnDateMs = new Date(returnDate).getTime();
      const currentDateMs = new Date().getTime();
      const differenceMs = returnDateMs - currentDateMs;
      const differenceDays = Math.ceil(differenceMs / (1000 * 60 * 60 * 24)) - 1;
      return differenceDays >= 0 ? differenceDays : 0;
    }
  },
  mounted() {
    this.fetchIssuedBooks();
  },
  components: {
    NavBar
  }
};
</script>

<style scoped>
.btn {
  display: flex;
  justify-content: center;
  background-color: coral;
  color: white;
  border: none;
  margin-left: 10px;
  margin-top: 5px;
  margin-bottom: 5px;
  padding: 5px 10px;
}

.btn:hover {
  background-color: #ff4500;
}

.ano {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 5px;
}


.book-cover {
  height: 150px;
  align-items: start;
  object-fit: contain;
  margin-bottom: 0.25rem;
}

.book-cover.disabled-image {
  opacity: 0.5;
}



.row {
  margin-left: 0.75%;
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
</style>
