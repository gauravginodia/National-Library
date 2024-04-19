<template>
  <div>
    <NavBar />

      
  <div class="card text-center mt-4 bg-dark text-white" style="width:40%;justify-content: center;margin-left:30%;margin-bottom: 2%;">
    <div class="card-body">
      <h5 class="card-title">Add Books to {{ name }} section</h5>
      <hr class="bg-white" />
      <div class="form">
      <form @submit.prevent="addBook">
        <div class="field">
          <label class="label">Book Title</label>
          <div class="control">
            <input v-model="newBook.title" class="input" type="text" placeholder="Book Title" required>
          </div>
        </div>

        <div class="field">
          <label class="label">Author Name</label>
          <div class="control">
            <input v-model="newBook.authorName" class="input" type="text" placeholder="Author Name" required>
          </div>
        </div>
        <div class="field">
          <label class="label">ISBN</label>
          <div class="control">
            <input v-model="newBook.isbn" class="input" placeholder="ISBN" required>
          </div>
        </div>
        <div class="field">
          <label class="label">Content</label>
          <div class="control">
            <textarea v-model="newBook.content" class="textarea" placeholder="Content" required></textarea>
          </div>
        </div>

      

        <button type="submit" class="btn btn-success rounded-pill px-4 py-2" style="border-color: aqua;">Add</button>
      </form>
    </div>
  </div>
</div>

   

              <hr>
                <h4 style="text-align: center;">{{name}} Books</h4>
           
              
                <div v-if="books.length > 0" style="width:100%">
                  <table class="center-table">
                    <thead>
                      <tr>
                        <th>Book Name</th>
                        <th>Author</th>
                        <th>ISBN</th>
                        <th>Function</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="book in books" :key="book.book_id">
                        <td v-if="book.editable">
                          <input v-model="book.book_name" class="form-control" type="text" required>
                        </td>
                        <td v-else>{{ book.book_name }}</td>
                        <td v-if="book.editable">
                          <input v-model="book.author" class="form-control" type="text" required>
                        </td>
                        <td v-else>{{ book.author }}</td>
                        <td v-if="book.editable">
                          <input v-model="book.isbn" class="form-control" type="text" required>
                        </td>
                        <td v-else>{{ book.isbn }}</td>
                        <td>
                          <div class="buttons">
                            <button v-if="book.editable" class="btn btn-primary" @click="saveChanges(book)">Save</button>
                            <button v-else class="btn btn-primary center" @click="toggleEditMode(book)">Edit</button>
                            <button class="btn btn-danger center" @click="deleteBook(book.book_id)">Delete</button>
                          </div>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <div v-else>
                  <p>This section has no books.Add some to view...</p>
                </div>
              
            </div>
          
     
 
</template>

<script>
import axios from "axios";
import NavBar from "../../components/NavBar.vue";

export default {
  name: "BooksbySection",
  props: ["id", "name"],
  data() {
    return {
      books: [],
      newBook: {
        title: "",
        authorName: "",
        content: "",
        section: "",
        isbn:"",
      },
    };
  },
  components: {
    NavBar,
  },
  methods: {
    async addBook() {
      try {
        this.newBook.section= this.name;
        const response = await axios.post(
          "http://127.0.0.1:5000/api/add/book",
          this.newBook,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        alert(response.data.message);
        this.newBook = {
          title: "",
          authorName: "",
          content: "",
          isbn:"",
          
        };
        this.fetchSectionBooks();
      } catch (error) {
          alert(error.response.data.error);
          
        
        console.error("Error adding book:", error);
      }
    },
    toggleEditMode(book) {
      book.editable = !book.editable;
    },
    async saveChanges(book) {
      try {
        const response = await axios.put(
          `http://127.0.0.1:5000/api/books/update`,
          {
            book_id: book.book_id,
            book_name: book.book_name,
            author: book.author,
            isbn: book.isbn,
          },
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        if (response.status === 200) {
          console.log("Book updated: ", response.data);
          alert("Book updated successfully!");
          book.editable = false;
          this.fetchSectionBooks();
        } else {
          console.error("Failed to update book: ", response.data.error);
        }
      } catch (error) {
        alert(error.response.data.error);
        console.error("Failed to update book: ", error.message);
      }
    },
    async fetchSectionBooks() {
      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/api/fetch/section/books",
          {
            section_id: this.id,
          },
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );

        if (response.status === 200) {
          console.log("Section Books:", response.data);
          this.books = response.data;
          this.books.forEach((book) => {
            book.editable = false;
          });
        } else {
          console.error("Failed to fetch section books: ", response.data.error);
        }
      } catch (error) {
          alert(error.response.data.error);
        console.error("Failed to fetch section books: ", error.message);
      }
    },
    async deleteBook(book_id) {
      try {
        const response = await axios.delete(
          `http://127.0.0.1:5000/api/books/delete`,
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
            data: { book_id: book_id },
          }
        );
        console.log(response.data);
        this.fetchSectionBooks();
      } catch (error) {
        alert(error.response.data.error);
        console.error("Failed to delete book: ", error.message);
      }
    },
  },
  mounted() {
    this.fetchSectionBooks();
  },
};
</script>

<style scoped>
.card.text-center.mt-4.bg-dark {
  border: 1px solid #333;
  border-radius: 0.5rem;
}

.card-title, .card-text {
  color: #fff;
}

.field {
  margin-bottom: 1rem;
}

.label {
  color: #fff;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.input,
.textarea {
  background-color: white;
  border: 1px solid #444;
  border-radius: 0.25rem;
  color: green;
  font-weight: bold;
  padding: 0.5rem;
  width: 100%;
}

.textarea {
  resize: vertical;
  min-height: 100px;
}

.btn-success {
  background-color: transparent;
  border:#fff;
  color: #fff;
  cursor: pointer;
}

.btn-success:hover {
  background-color: #1e7c31;
}

.form {
  background:rgba(#13232f,.9);
  padding: 20px;
  max-width:600px;
  border-radius:4px;
  box-shadow:0 4px 10px 4px rgba(#13232f,.3);
}
.add-sections {
  display: flex;
  justify-content: center;
  align-items: center;
}

.delete {
  margin: 10px 10px;
  color: white;
  background-color: #f13535;
}

.delete:hover {
  background-color: #aa0000;
}

.btn {

  justify-content: space-around;
  align-items: center;
  padding: 5%;
  margin:2%;
}


*, *:before, *:after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}


table {
  width:100%;
  background: #333;
  border-radius: 0.25em;
  border-collapse: collapse;
  margin: 1em;
}
th {
  border-bottom: 1px solid #364043;
  color: #E2B842;
  font-size: 0.85em;
  font-weight: 600;
  padding: 0.5em 1em;
  text-align: left;
}
td {
  color: #fff;
  font-weight: 400;
  padding: 0.65em 1em;
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
