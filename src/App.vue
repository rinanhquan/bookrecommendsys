
<template>
  <div id="app" name="app">
    <el-container>
      <!-- Top navigation bar -->
      <div class="topbar">
        <div class="nav">
          <ul>
            <li v-if="!this.$store.getters.getUser">
              <el-button type="text" @click="login">Log In</el-button>
              <span class="sep">|</span>
              <el-button type="text" @click="register = true">Register</el-button>
            </li>
            <li v-else>
              Welcome
              <el-popover placement="top" width="180" v-model="visible">
                <p>Are you sure to log out?</p>
                <div style="text-align: right; margin: 10px 0 0">
                  <el-button size="mini" type="text" @click="visible = false">Cancel</el-button>
                  <el-button type="primary" size="mini" @click="logout">Sure</el-button>
                </div>
                <el-button type="text" slot="reference">{{this.$store.getters.getUser.userName}}</el-button>
              </el-popover>
            </li>
            <li :class="getNum > 0 ? 'shopCart-full' : 'shopCart'">
              <router-link to="/shoppingCart">
                <i class="el-icon-shopping-cart-full"></i> Shopping Cart
                <span class="num">({{getNum}})</span>
              </router-link>
            </li>
          </ul>
        </div>
      </div>

      <el-header>
        <el-menu
          :default-active="activeIndex"
          class="el-menu-demo"
          mode="horizontal"
          active-text-color="#409eff"
          router
        >
          <div class="logo">
            <router-link to="/">
              <img width="189" height="59" src="../public/imgs/logo.jpg" alt />
            </router-link>
          </div>
          <el-menu-item index="/">Home</el-menu-item>
          <el-menu-item index="/goods">All Products</el-menu-item>
          <el-menu-item index="/about">About Us</el-menu-item>

          <div class="so">
            <el-input placeholder="Please input searching context" v-model="search">
              <el-button slot="append" icon="el-icon-search" @click="searchClick"></el-button>
            </el-input>
          </div>
        </el-menu>
      </el-header>

      <MyLogin></MyLogin>

      <MyRegister :register="register" @fromChild="isRegister"></MyRegister>


      <el-main>
        <keep-alive>
          <router-view></router-view>
        </keep-alive>
      </el-main>


      <el-footer>
        <div class="footer">
          <div class="ng-promise-box">
            <div class="ng-promise">
              <p class="text">
                <a class="icon1" href="javascript:;">7 days no reason to return</a>
                <a class="icon2" href="javascript:;">Free shipping on orders over 99$</a>
                <a class="icon3" style="margin-right: 0" href="javascript:;">100% Quality Assurance</a>
              </p>
            </div>
          </div>
          <div class="github">
            <a href="#" target="_blank">
              <div class="github-but"></div>
            </a>
          </div>
          <div class="mod_help">
            <p>
              <router-link to="/">Home</router-link>
              <span>|</span>
              <router-link to="/goods">All Products</router-link>
              <span>|</span>
              <router-link to="/about">About Us</router-link>
            </p>
            <p class="coty">Copyright by Anh Quan &copy; 2022-2023</p>
          </div>
        </div>
      </el-footer>

    </el-container>
  </div>
</template>

<script>
import { mapActions } from "vuex";
import { mapGetters } from "vuex";

export default {
  beforeUpdate() {
    this.activeIndex = this.$route.path;
  },
  data() {
    return {
      activeIndex: "", 
      search: "", 
      register: false, 
      visible: false 
    };
  },
  created() {
    if (localStorage.getItem("user")) {
      this.setUser(JSON.parse(localStorage.getItem("user")));
    }
  },
  computed: {
    ...mapGetters(["getUser", "getNum"])
  },
  watch: {
    getUser: function(val) {
      if (val === "") {
        this.setShoppingCart([]);
      } else {
        this.$axios
          .post("/api/user/shoppingCart/getShoppingCart?user_id="+val.user_id, 
          )
          .then(res => {
            if (res.data.code === "001") {
              this.setShoppingCart(res.data.shoppingCartData);
            } else {
              this.notifyError(res.data.msg);
            }
          })
          .catch(err => {
            return Promise.reject(err);
          });
      }
    }
  },
  methods: {
    ...mapActions(["setUser", "setShowLogin", "setShoppingCart"]),
    login() {
      this.setShowLogin(true);
    },
    logout() {
      this.visible = false;
      localStorage.setItem("user", "");
      this.setUser("");
      this.notifySucceed("Goodbye");
      location.reload()
    },
    isRegister(val) {
      this.register = val;
    },

    searchClick() {
      if (this.search != "") {

        this.$router.push({ path: "/goods", query: { search: this.search } });
        this.search = "";
      }
    }
  }
};
</script>

<style>

* {
  padding: 0;
  margin: 0;
  border: 0;
  list-style: none;
}
#app .el-header {
  padding: 0;
}
#app .el-main {
  min-height: 300px;
  padding: 20px 0;
}
#app .el-footer {
  padding: 0;
}
a,
a:hover {
  text-decoration: none;
}

.topbar {
  height: 40px;
  background-color: #3d3d3d;
  margin-bottom: 20px;
}
.topbar .nav {
  width: 1225px;
  margin: 0 auto;
}
.topbar .nav ul {
  float: right;
}
.topbar .nav li {
  float: left;
  height: 40px;
  color: #b0b0b0;
  font-size: 14px;
  text-align: center;
  line-height: 40px;
  margin-left: 20px;
}
.topbar .nav .sep {
  color: #b0b0b0;
  font-size: 12px;
  margin: 0 5px;
}
.topbar .nav li .el-button {
  color: #b0b0b0;
}
.topbar .nav .el-button:hover {
  color: #fff;
}
.topbar .nav li a {
  color: #b0b0b0;
}
.topbar .nav a:hover {
  color: #fff;
}
.topbar .nav .shopCart {
  width: 180px;
  background: #424242;
}
.topbar .nav .shopCart:hover {
  background: #fff;
}
.topbar .nav .shopCart:hover a {
  color: #ff6700;
}
.topbar .nav .shopCart-full {
  width: 120px;
  background: #ff6700;
}
.topbar .nav .shopCart-full a {
  color: white;
}

.el-header .el-menu {
  max-width: 1225px;
  margin: 0 auto;
}
.el-header .logo {
  height: 60px;
  width: 189px;
  float: left;
  margin-right: 100px;
}
.el-header .so {
  margin-top: 10px;
  width: 300px;
  float: right;
}

.footer {
  width: 100%;
  text-align: center;
  background: #2f2f2f;
  padding-bottom: 20px;
}
.footer .ng-promise-box {
  border-bottom: 1px solid #3d3d3d;
  line-height: 145px;
}
.footer .ng-promise-box {
  margin: 0 auto;
  border-bottom: 1px solid #3d3d3d;
  line-height: 145px;
}
.footer .ng-promise-box .ng-promise p a {
  color: #fff;
  font-size: 20px;
  margin-right: 210px;
  padding-left: 44px;
  height: 40px;
  display: inline-block;
  line-height: 40px;
  text-decoration: none;
  background: url("./assets/imgs/us-icon.png") no-repeat left 0;
}
.footer .github {
  height: 50px;
  line-height: 50px;
  margin-top: 20px;
}
.footer .github .github-but {
  width: 50px;
  height: 50px;
  margin: 0 auto;
  background: url("./assets/imgs/logo.jpg") no-repeat;
}
.footer .mod_help {
  text-align: center;
  color: #888888;
}
.footer .mod_help p {
  margin: 20px 0 16px 0;
}

.footer .mod_help p a {
  color: #888888;
  text-decoration: none;
}
.footer .mod_help p a:hover {
  color: #fff;
}
.footer .mod_help p span {
  padding: 0 22px;
}

</style>