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
        <form method="POST" @submit.prevent="updateUserVariable">
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
                      name="variable_name"
                      v-model="variable_name"
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
                      name="variable_value"
                      v-model="variable_value"
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
                      name="user_email"
                      v-model="user_email"
                    />
                  </div>

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
import CTFd from "core/CTFd";
import { bindMarkdownEditor } from "../../styles";

export default {
  name: "UserVariableEditForm",
  props: {
    challenge_id: Number,
    uservariable_id: Number,
    uservariables: Array
  },
  data: function() {
    return {
      user_email: null,
      variable_name: null,
      variable_value: null, 
    };
  },
  watch: {
    uservariable_id: {
      immediate: true,
      handler(val, oldVal) {
        if (val !== null) {
          this.loadUserVariable();
        }
      }
    }
  },

  methods: {
    loadUserVariable: function() {
      CTFd.fetch(`/api/v1/uservariables/${this.$props.uservariable_id}?preview=true`, {
        method: "GET",
        credentials: "same-origin",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json"
        }
      })
        .then(response => {
          return response.json();
        })
        .then(response => {
          if (response.success) {
            let uservariable = response.data;
            this.user_email = uservariable.user_email;
            this.variable_name = uservariable.variable_name;
            this.variable_value = uservariable.variable_value;
            
          }
        });
    },

    updateUserVariable: function() {
      let params = {
        challenge_id: this.$props.challenge_id,
        user_id: this.user_id,
        variable_name: this.variable_name,
        variable_value: this.variable_value
      };

      CTFd.fetch(`/api/v1/uservariables/${this.$props.uservariable_id}`, {
        method: "PATCH",
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
  },
  mounted() {
    if (this.uservariable_id) {
      this.loadUserVariable();
    }
  },
  created() {
    if (this.uservariable_id) {
      this.loadUserVariable();
    }
  }
};
</script>

<style scoped></style>
