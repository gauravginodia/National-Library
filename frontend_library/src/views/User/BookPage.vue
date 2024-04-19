<template>
    <div>
      <NavBar />
      <div class="product-page">
        <div class="container product-details-container">
          <div class="row justify-content-center">
            <div class="col-md-4 product-image">
              <img :src="book.coverUrl" alt="Book Cover" class="img-fluid">
              <div class="text-center">
    <button v-if="book.button_text === 'Request'"
            class="btn btn-primary"
            @click="handleButtonClick(book)">
        {{ book.button_text }}
    </button>
    <button v-else-if="book.button_text === 'Return'"
            class="btn btn-danger"
            @click="handleButtonClick(book)">
        {{ book.button_text }}
    </button>
    <button v-else-if="book.button_text === 'Requested'"
            class="btn btn-warning"
            disabled
            @click="handleButtonClick(book)">
        {{ book.button_text }}
    </button>
</div>
            </div>
            <div class="col-md-8 product-details">
              <div>
                <h2>{{ book.name }}</h2>
                <h4 class="text-muted">by {{ book.authors }}</h4>
                <span v-for="star in book.rating" :key="star" style="font-size: smaller;">⭐</span>
                <hr style="margin-top: 0%;">
                <p class="text-justify" style="margin-top: 1%;">{{ book.content }}</p>
                <div>
                  <h4 class="mt-4">Reviews:</h4>
                  <div v-if="bookFeedback.length > 0">
                    <table class="table">
                      <thead>
                        <tr>
                          <th>User Name</th>
                          <th>Feedback</th>
                          <th>Rating</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="feedback in bookFeedback" :key="feedback.id">
                          <td>{{ feedback.username }}</td>
                          <td>{{ feedback.feedback }}</td>
                          <td>
                            <span v-for="i in feedback.rating" :key="i">⭐</span>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                  <div v-else>
                    <p>No feedback yet. Be the first one to comment!</p>
                  </div>
                  <!-- Add Feedback Form -->
                  <div class="review-box">
                    <h4>Write a Review</h4>
                    <form @submit.prevent="submitFeedback">
                      <div class="form-group">
                        <label for="feedback">Add Feedback:</label>
                        <textarea id="feedback" class="form-control" v-model="newFeedback"></textarea>
                      </div>
                      <div class="form-group">
                        <label>Rating:</label>
                        <div class="rating-buttons">
                          <button
                            v-for="i in 5"
                            :key="i"
                            type="button"
                            class="btn btn-outline-secondary"
                            :class="{ 'btn-warning': i <= newRating }"
                            @click="setRating(i)"
                          >
                            {{ i }}
                          </button>
                        </div>
                      </div>
                      <button type="submit" class="btn btn-primary mx-auto d-block" style="text-align: center;margin-top: 4%;">Submit Review</button>
                    </form>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <hr>
      <div class="similar-books">
        <h2 style="text-align: center;">Readers also viewed </h2>
        <div class="similar-books-list">
          <div v-for="book in sectionbooks" :key="book.id" class="similar-book">
            <button @click="readBook(book.id)" style="border: none;">
            <template v-if="book.coverUrl">
            <img :src="book.coverUrl" alt="Book Cover" class="img-fluid">
            </template>
            <template v-else>
              <img src="@/assets/default.jpeg" alt="Book Cover" class="img-fluid">
            </template>
          </button>
            <p>by {{ book.authors }}</p>
           
          </div>
        </div>
        <button class="scroll-button prev" @click="scrollHorizontal(-1)">
          <i class="bi bi-arrow-left"></i>
        </button>
        <button class="scroll-button next" @click="scrollHorizontal(1)">
          <i class="bi bi-arrow-right"></i>
        </button>
      </div>
    </div>
  </template>
  
  

  <script>
  import NavBar from "../../components/NavBar.vue";
  import axios from "axios";

  
  export default {
    name: "ProductPage",
    components: {
      NavBar
    },
    data() {
      return {
        book: {},
        bookFeedback: [],
        similarBooks: [],
        newFeedback: "",
        newRating: null,
        sectionbooks:[]
      };
    },
    computed: {
      buttonColor() {
        if (this.book.is_allocated) {
          return "blue-button";
        } else if (this.book.is_requested) {
          return "blue-button";
        } else {
          return "yellow-button";
        }
      },
      isButtonDisabled() {
        return this.book.is_allocated || this.book.is_requested;
      }
    },
    methods: {
      readBook(book_id) {
      this.$router.push({ name: 'BookPage', params: { id: book_id} });

    },
      async fetchBookDetails() {
        try {
          const bookId = this.$route.params.id;
          const response = await axios.get(`http://127.0.0.1:5000/api/books/${bookId}`, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          });
          this.book = response.data;
          await this.fetchBookCovers(this.book);
          await this.fetchsectionBooks(this.book.section_id);
          await this.fetchBookFeedback(this.book.id);
        } catch (error) {
          console.error("Error fetching book details:", error);
        }
      },
      async fetchBookCovers(books) {
        try {
          console.log(books);
          const coverUrl = await this.getBookCover(books);
          books.coverUrl = coverUrl;
          return books.coverurl;
        } catch (error) {
          console.error("Error fetching book cover:", error);
          books.coverUrl = null;
        }
  
      },
      async multiplecover(books) {
        for (const book of books) {
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
            return response.data;
          })
          .catch((error) => {
            console.error("Error fetching book cover:", error);
            return null;
          });
      },
  
      async fetchBookFeedback(book_id) {
        try {
          const bookId = book_id;
          const response = await axios.get(`http://127.0.0.1:5000/api/books/${bookId}/feedback`, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          });
          this.bookFeedback = response.data;
          
        } catch (error) {
          console.error("Error fetching book feedback:", error);
        }
      },
  
      downloadBook() {
        // Implement book download logic
      },
      async submitFeedback() {
        try {
          const response = await axios.post(
            "http://127.0.0.1:5000/api/submit_feedback",
            {
              rating: this.newRating,
              feedback: this.newFeedback,
              user_id: this.book.user_id, 
              book_id: this.book.id 
            },
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              },
            }
          );
          if (response.status === 200) {
            console.log("Feedback submitted successfully");
            this.newRating = null;
            this.newFeedback = "";
            alert("Feedback submitted successfully");
            location.reload(); // Refresh the page
          } else {
            console.error("Failed to submit feedback");
          }
        } catch (error) {
          alert(error.response.data.error);
          console.error("Error submitting feedback:", error);
        }
      },
      async fetchsectionBooks(id) {
        try {
          const section_id = id;
          const response = await axios.get(`http://127.0.0.1:5000/api/sections/${section_id}/books`, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          });
          this.sectionbooks = response.data;
          await this.multiplecover(this.sectionbooks);
        } catch (error) {
          console.error("Error fetching book feedback:", error);
        }
      },
      scrollHorizontal(direction) {
        const scrollContainer = document.querySelector(".similar-books-list");
        const scrollAmount = 300 * direction;
        scrollContainer.scrollBy({
          left: scrollAmount,
          behavior: "smooth"
        });
      },
  
      setRating(rating) {
        this.newRating = rating;
      },
  
    async  handleButtonClick() {
        // Handle button click based on conditions
        if (this.book.is_allocated) {
          try {
        const response = await axios.post(
          "http://127.0.0.1:5000/api/return/book",
          {
            book_id: this.book.id,
            user_id: this.book.user_id
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`
            }
          }
        );
        if (response.status === 200) {
          alert("Book has been returned");
          console.log("Book returned successfully");
          this.fetchBookDetails();
        } else {
          console.error("Failed to return the book");
        }
      } catch (error) {
        console.error("Error returning the book:", error);
      }
        }else {
      
      const requestData = {
        book_id: this.book.id,
      };
      await axios
        .post("http://127.0.0.1:5000/api/request/book", requestData, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        })
        .then((response) => {
          console.log(response.data);
          console.log("Request sent");
          this.fetchBookDetails();
        })
        .catch((error) => {
          alert(error.response.data.error);
          console.log(error);
        });
    }
        },
     
  
      getButtonLabel() {
        if (this.book.is_allocated) {
          return "Return";
        } else if (this.book.is_requested) {
          return "Requested";
        } else {
          return "Request";
        }
      },
    },
  //   beforeRouteUpdate(to, from, next) {
  //   // Call fetchBookDetails when route parameters change
  //   this.fetchBookDetails();
  //   next();
  // },
  mounted() {
    // Fetch initial book details when the component is mounted
    this.fetchBookDetails();
  },
  watch: {
    // Watch for changes in route parameters
    '$route'() {
      // Call fetchBookDetails when the route changes
      this.fetchBookDetails();
    }
  }
};
  </script>
  
  <style scoped>
  .product-page {
      padding: 20px;
      margin-bottom: 2%;
  }
  
  .product-details-container {
      background-color: #fff;
      padding: 20px;
      border-radius: 10px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }
  
  .product-image img {
      width: 100%;
      height: auto;
  }
  
  .download-button {
      background-color: #007bff;
      color: #fff;
      border: none;
      padding: 10px 20px;
      cursor: pointer;
  }
  
  .blue-button {
      background-color: #007bff;
      color: #fff;
  }
  
  .yellow-button {
      background-color: #ffc107;
      color: #000;
  }
  
  .blue-button:disabled,
  .yellow-button:disabled {
      opacity: 0.5;
      cursor: not-allowed;
  }
  
  .similar-books {
      position: relative;
      margin-top: 3%;
  }
  
  .similar-books p {
      text-align: center;
  }
  
  .similar-books-list {
      display: flex;
      flex-wrap: nowrap;
      overflow-x: auto;
      padding-bottom: 20px;
      scrollbar-width: none;
      -ms-overflow-style: none;
  }
  
  .similar-books-list::-webkit-scrollbar {
      display: none;
  }
  
  .similar-book {
      max-width: 13.333%;
      padding: .75rem;
      margin-bottom: 2rem;
      border: 0;
      flex-basis: 33.333%;
      flex-grow: 0;
      flex-shrink: 0;
  }
  
  .similar-book img {
      width: 100%;
      height: 80%;
  }
  
  .scroll-button {
      position: absolute;
      top: 50%;
      transform: translateY(-50%);
      background: transparent;
      border: none;
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
  
  .star {
      font-size: 24px;
      color: #FFD700;
      cursor: pointer;
  }
  
  .review-box {
      position: relative;
      border: 1px solid #ccc;
      border-radius: 5px;
      padding: 20px;
      width: 300px;
      margin-top: 100px;
  }
  
  .rating-buttons {
      display: flex;
      justify-content: center;
      margin-top: 10px;
      color: black;
      margin-top: 1%;
  }
  
  .rating-buttons :hover {
      background-color: #FFD700;
      color: black;
  }
  </style>
  