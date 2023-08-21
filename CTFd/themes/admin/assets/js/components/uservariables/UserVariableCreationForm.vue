<template>
  <div class="modal fade" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header text-center">
          <div class="container">
            <div class="row">
              <div class="col-md-12">
                <h3>User Variable</h3>
              </div>
            </div>
          </div>
          <button
            type="button"
            class="close"
            data-dismiss="modal"
            aria-label="Close"
          >
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <form method="POST" @submit.prevent="submitUserVariable">
          <div class="modal-body">
            <div class="container">
              <div class="row">
                <div class="col-md-12">
                  <div class="form-group">
                    <label>
                      Variable Name<br />
                      <small>Enter the variable name you have included in the markdown of the Challenge description</small>
                    </label>
                    <input
                      type="string"
                      class="form-control"
                      v-model="variable_name"
                      name="variable_name"
                      
                    />
                  </div>
                  <div class="form-group">
                    <label>
                      Variable Value<br />
                      <small>Enter the value for variable you mentioned above</small>
                    </label>
                    <input
                      type="string"
                      class="form-control"
                      v-model="variable_value"
                      name="variable_value"
                    />
                  </div>
                  <div class="form-group">
                    <label>
                      User Email<br />
                      <small>Enter the user email for which this variable is valid.</small>
                    </label>
                    <input
                      type="string"
                      class="form-control"
                      v-model="user_email"
                      name="user_email"
                    />
                  </div>
                  <input type="hidden" id="uservariable-id-for-uservariable" name="id" />
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <div class="container">
              <div class="row">
                <div class="col-md-12">
                  <button class="btn btn-primary float-right">Submit</button>
                </div>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import $ from "jquery";
export default {
  name: "UserVariableCreationForm",
  props: {
    challenge_id: Number,
    uservariables: Array
  },
  data: function() {
    return {
      useremail: null,
    };
  },
  methods: {
    submitUserVariable: function() {
      let params = {
        user_email: this.user_email,
        challenge_id: this.$props.challenge_id,
        variable_name: this.variable_name,
        variable_value: this.variable_value
      };
      CTFd.fetch("/api/v1/uservariables", {
        method: "POST",
        credentials: "same-origin",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json"
        },
        body: JSON.stringify(params)
      })
        .then(response => {
          return response.json();
        })
        .then(response => {
          if (response.success) {
            this.$emit("refreshUserVariables", this.$options.name);
          }
        });
    }
  }
};
</script>

<style scoped></style>
