<template>
  <div>
    <NavBar />
<h2 style="text-align: center;margin-top:1%">Requested Books</h2>

  <div v-if="listrequested.length > 0">
    <table class="table center-table">
      <thead>
        <tr>
          <th>Book Name</th>
          <th>Requested By</th>
          <th>Grant</th>
          <th>Reject</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="book in listrequested" :key="book.book_id">
          <td>{{ book.book_name }}</td>
          <td>{{ book.user_name }}</td>
          <td>
            <button class="btn btn-success" @click="
              approve(
                book.book_id,
                book.user_id
              )
              ">
              Grant
            </button>
          </td>
          <td>
            <button class="btn btn-danger" @click="takeback(book.allocation_id)">
              Reject
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  <div v-else>
    <p>You have no pending requests</p>
  </div>

</div>
</template>

<script>
import NavBar from "../../components/NavBar.vue";
export default {
  name: "RequestedReading",
  components: {
    NavBar,
  },
  data() {
    return {
      listrequested: [],
    };
  },
  mounted() {
    this.listofbooks();
  },
  methods: {
    async listofbooks() {
      try {
        const response = await fetch(
          "http://127.0.0.1:5000/api/books/requested",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        const data = await response.json();
        if (response.ok) {
          this.listrequested = data;
          console.log("Requested books: ", data);
        } else {
          console.error("Failed to fetch requested books: ", data.error);
        }
      } catch (error) {
        console.error("Error fetching requested books: ", error);
      }
    },
    async approve(bookId, userId) {
      try {
        console.log(userId);
        const response = await fetch(
          "http://127.0.0.1:5000/api/books/allocate",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
            body: JSON.stringify({
              book_id: bookId,
              user_id: userId,
            }),
          }
        );
        const data = await response.json();
        if (response.ok) {
          console.log("Book has been granted", data.message);
          this.listofbooks();
        } else {
          console.error("Some error occured ", data.error);
        }
      } catch (error) {
        console.error("Error: ", error);
      }
    },
    async takeback(allocationId) {
      try {
        const response = await fetch(
          "http://127.0.0.1:5000/api/delete/request",
          {
            method: "DELETE",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
            body: JSON.stringify({
              allocation_id: allocationId,
            }),
          }
        );


        if (!response.ok) {
          throw new Error("Failed to revoke access");
        }
        else {
          this.listofbooks();
        }

        const data = await response.json();
        console.log(data);
      } catch (error) {
        console.error("Error revoking access:", error);
      }
    },
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
  margin-left: 5%;
  margin-top: 2%;
}

th {
  border-bottom: 1px solid #364043;
  color: #E2B842;
  font-size: large;
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
