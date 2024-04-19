<template>
  <NavBar />
  <div>
  <h2 style="text-align: center;margin-top:2.5%">Allocated Books</h2>


  <div v-if="listallocated.length > 0">
    <table class="table center-table">
      <thead>
        <tr>
          <th>Book Name</th>
          <th>User Name</th>
          <th>Date & Time of Issue</th>
          <th>Return Date</th>
          <th>Days Left</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="book in listallocated" :key="book.book_id">
          <td>{{ book.book_name }}</td>
          <td>{{ book.user_name }}</td>
          <td>{{ book.date_of_issue }}</td>
          <td>{{ book.return_date }}</td>
          <td>{{ calculateDaysLeft(book.return_date) }}</td>
          <td>
            <button class="btn btn-danger mw-100" @click="
              takeawayaccess(book.allocation_id, book.book_id, book.user_id)
              ">
              Revoke
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  <div v-else>
    <p>User has not beein assigned any book yet</p>
  </div>

</div>
</template>

<script>
import NavBar from "../../components/NavBar.vue";
import axios from "axios";
export default {
  name: "AssignedBooks",
  components: {
    NavBar,
  },
  data() {
    return {
      listallocated: [],
    };
  },
  created() {
    this.listofallocatedbooks();
  },
  methods: {
    async listofallocatedbooks() {
      try {
        const headers = new Headers();
        headers.append("Content-Type", "application/json");
        headers.append(
          "Authorization",
          `Bearer ${localStorage.getItem("accessToken")}`
        );

        const response = await fetch(
          "http://127.0.0.1:5000/api/librarian/allocated_books",
          {
            method: "PUT",
            headers: headers,
          }
        );

        if (!response.ok) {
          throw new Error("Failed to fetch allocated books");
        }

        const data = await response.json();
        this.listallocated = data;
        console.log(this.listallocated);
        console.log(data);
      } catch (error) {
        console.error("Error:", error.message);
      }
    },

    async takeawayaccess(allocation_id, book_id, user_id) {
      try {
        const headers = {
          Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
        };

        const response = await axios.post(
          "http://127.0.0.1:5000/api/revoke/book",
          {
            allocation_id: allocation_id,
            book_id: book_id,
            user_id: user_id,
          },
          { headers: headers }
        );

        if (response.status === 200) {
          console.log("Book returned successfully");
          this.listofallocatedbooks();
        } else {
          console.error("Failed to return the book");
        }
      } catch (error) {
        console.error("Error returning the book:", error);
      }
    }
    ,
    calculateDaysLeft(returnDate) {
      const returnDateMs = new Date(returnDate).getTime();
      const currentDateMs = new Date().getTime();
      const differenceMs = returnDateMs - currentDateMs;
      const differenceDays = (Math.ceil(differenceMs / (1000 * 60 * 60 * 24))) - 1;
      return differenceDays >= 0 ? differenceDays : 0;
    }
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