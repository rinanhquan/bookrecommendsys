<template>
  <div class="shoppingCart">
    <div class="cart-header">
      <div class="cart-header-content">
        <p>
          <i class="el-icon-shopping-cart-full" style="color:#ff6700; font-weight: 600;"></i>
          My Cart
        </p>
        <span>Reminder: Whether the product is successfully purchased is subject to the final order, please settle as soon as possible</span>
      </div>
    </div>
    <div class="content" v-if="getShoppingCart.length>0">
      <ul>
        <li class="header">
          <div class="pro-check">
            <el-checkbox v-model="isAllCheck">Select All</el-checkbox>
          </div>
          <div class="pro-img"></div>
          <div class="pro-name">Product Name</div>
          <div class="pro-price">Unit Price</div>
          <div class="pro-num">Quantity</div>
          <div class="pro-total">Subtotal</div>
          <div class="pro-action">Operate</div>
        </li>
        <li class="product-list" v-for="(item,index) in getShoppingCart" :key="item.id">
          <div class="pro-check">
            <el-checkbox :value="item.check" @change="checkChange($event,index)"></el-checkbox>
          </div>
          <div class="pro-img">
            <router-link :to="{ path: '/goods/details', query: {productID:item.productID} }">
          
              <img :src="item.productImg" />
            </router-link>
          </div>
          <div class="pro-name">
            <router-link
              :to="{ path: '/goods/details', query: {productID:item.productID} }"
            >{{item.productName}}</router-link>
          </div>
          <div class="pro-price">{{item.price}}$</div>
          <div class="pro-num">
            <el-input-number
              size="small"
              :value="item.num"
              @change="handleChange($event,index,item.productID)"
              :min="1"
              :max="item.maxNum"
            ></el-input-number>
          </div>
          <div class="pro-total pro-total-in">{{item.price*item.num}}$</div>
          <div class="pro-action">
            <el-popover placement="right">
              <p>Confirm To Delete? </p>
              <div style="text-align: right; margin: 10px 0 0">
                <el-button
                  type="primary"
                  size="mini"
                  @click="deleteItem($event,item.id,item.productID)"
                >Sure</el-button>
              </div>
              <i class="el-icon-error" slot="reference" style="font-size: 18px;"></i>
            </el-popover>
          </div>
        </li>
      </ul>
      <div style="height:20px;background-color: #f5f5f5"></div>
      <div class="cart-bar">
        <div class="cart-bar-left">
          <span>
            <router-link to="/goods">Continue Shopping</router-link>
          </span>
          <span class="sep">|</span>
          <span class="cart-total">
            common
            <span class="cart-total-num">{{getNum}}</span> items, selected
            <span class="cart-total-num">{{getCheckNum}}</span> item
          </span>
        </div>
        <div class="cart-bar-right">
          <span>
            <span class="total-price-title">Total: </span>
            <span class="total-price">{{getTotalPrice}}$</span>
          </span>
          <router-link :to="getCheckNum > 0 ? '/confirmOrder' : ''">
            <div :class="getCheckNum > 0 ? 'btn-primary' : 'btn-primary-disabled'">Order</div>
          </router-link>
        </div>
      </div>
    </div>
    <div v-else class="cart-empty">
      <div class="empty">
        <h2>Your cart is still empty! </h2>
        <p>Go shopping! </p>
      </div>
    </div>
  </div>
</template>
<script>
import { mapActions } from "vuex";
import { mapGetters } from "vuex";

export default {
  data() {
    return {};
  },
  methods: {
    ...mapActions(["updateShoppingCart", "deleteShoppingCart", "checkAll"]),
    handleChange(currentValue, key, productID) {
      this.updateShoppingCart({ key: key, prop: "check", val: true });
      this.$axios
        .post("/api/user/shoppingCart/updateShoppingCart", {
          user_id: this.$store.getters.getUser.user_id,
          product_id: productID,
          num: currentValue
        })
        .then(res => {
          switch (res.data.code) {
            case "001":
              this.updateShoppingCart({
                key: key,
                prop: "num",
                val: currentValue
              });
              this.notifySucceed(res.data.msg);
              break;
            default:
              this.notifyError(res.data.msg);
          }
        })
        .catch(err => {
          return Promise.reject(err);
        });
    },
    checkChange(val, key) {
      this.updateShoppingCart({ key: key, prop: "check", val: val });
    },
    deleteItem(e, id, productID) {
      this.$axios
        .post("/api/user/shoppingCart/deleteShoppingCart", {
          user_id: this.$store.getters.getUser.user_id,
          product_id: productID
        })
        .then(res => {
          switch (res.data.code) {
            case "001":
              this.deleteShoppingCart(id);
              this.notifySucceed(res.data.msg);
              break;
            default:
              this.notifyError(res.data.msg);
          }
        })
        .catch(err => {
          return Promise.reject(err);
        });
    }
  },
  computed: {
    ...mapGetters([
      "getShoppingCart",
      "getCheckNum",
      "getTotalPrice",
      "getNum"
    ]),
    isAllCheck: {
      get() {
        return this.$store.getters.getIsAllCheck;
      },
      set(val) {
        this.checkAll(val);
      }
    }
  }
};
</script>
<style scoped>
.shoppingCart {
  background-color: #f5f5f5;
  padding-bottom: 20px;
}

.shoppingCart .cart-header {
  height: 64px;
  border-bottom: 2px solid #ff6700;
  background-color: #fff;
  margin-bottom: 20px;
}
.shoppingCart .cart-header .cart-header-content {
  width: 1225px;
  margin: 0 auto;
}
.shoppingCart .cart-header p {
  font-size: 28px;
  line-height: 58px;
  float: left;
  font-weight: normal;
  color: #424242;
}
.shoppingCart .cart-header span {
  color: #757575;
  font-size: 12px;
  float: left;
  height: 20px;
  line-height: 20px;
  margin-top: 30px;
  margin-left: 15px;
}

.shoppingCart .content {
  width: 1225px;
  margin: 0 auto;
  background-color: #fff;
}

.shoppingCart .content ul {
  background-color: #fff;
  color: #424242;
  line-height: 85px;
}

.shoppingCart .content ul .header {
  height: 85px;
  padding-right: 26px;
  color: #424242;
}
.shoppingCart .content ul .product-list {
  height: 85px;
  padding: 15px 26px 15px 0;
  border-top: 1px solid #e0e0e0;
}
.shoppingCart .content ul .pro-check {
  float: left;
  height: 85px;
  width: 110px;
}
.shoppingCart .content ul .pro-check .el-checkbox {
  font-size: 16px;
  margin-left: 24px;
}
.shoppingCart .content ul .pro-img {
  float: left;
  height: 85px;
  width: 120px;
}
.shoppingCart .content ul .pro-img img {
  height: 80px;
  width: 80px;
}
.shoppingCart .content ul .pro-name {
  float: left;
  width: 380px;
}
.shoppingCart .content ul .pro-name a {
  color: #424242;
}
.shoppingCart .content ul .pro-name a:hover {
  color: #ff6700;
}
.shoppingCart .content ul .pro-price {
  float: left;
  width: 140px;
  padding-right: 18px;
  text-align: center;
}
.shoppingCart .content ul .pro-num {
  float: left;
  width: 150px;
  text-align: center;
}
.shoppingCart .content ul .pro-total {
  float: left;
  width: 120px;
  padding-right: 81px;
  text-align: right;
}
.shoppingCart .content ul .pro-total-in {
  color: #ff6700;
}
.shoppingCart .content ul .pro-action {
  float: left;
  width: 80px;
  text-align: center;
}
.shoppingCart .content ul .pro-action i:hover {
  color: #ff6700;
}

.shoppingCart .cart-bar {
  width: 1225px;
  height: 50px;
  line-height: 50px;
  background-color: #fff;
}
.shoppingCart .cart-bar .cart-bar-left {
  float: left;
}
.shoppingCart .cart-bar .cart-bar-left a {
  line-height: 50px;
  margin-left: 32px;
  color: #757575;
}
.shoppingCart .cart-bar .cart-bar-left a:hover {
  color: #ff6700;
}
.shoppingCart .cart-bar .cart-bar-left .sep {
  color: #eee;
  margin: 0 20px;
}
.shoppingCart .cart-bar .cart-bar-left .cart-total {
  color: #757575;
}
.shoppingCart .cart-bar .cart-bar-left .cart-total-num {
  color: #ff6700;
}
.shoppingCart .cart-bar .cart-bar-right {
  float: right;
}
.shoppingCart .cart-bar .cart-bar-right .total-price-title {
  color: #ff6700;
  font-size: 14px;
}
.shoppingCart .cart-bar .cart-bar-right .total-price {
  color: #ff6700;
  font-size: 30px;
}
.shoppingCart .cart-bar .cart-bar-right .btn-primary {
  float: right;
  width: 200px;
  text-align: center;
  font-size: 18px;
  margin-left: 50px;
  background: #ff6700;
  color: #fff;
}
.shoppingCart .cart-bar .cart-bar-right .btn-primary-disabled {
  float: right;
  width: 200px;
  text-align: center;
  font-size: 18px;
  margin-left: 50px;
  background: #e0e0e0;
  color: #b0b0b0;
}
.shoppingCart .cart-bar .cart-bar-right .btn-primary:hover {
  background-color: #f25807;
}

.shoppingCart .cart-empty {
  width: 1225px;
  margin: 0 auto;
}
.shoppingCart .cart-empty .empty {
  height: 300px;
  padding: 0 0 130px 558px;
  margin: 65px 0 0;
  background: url(../assets/imgs/cart-empty.png) no-repeat 124px 0;
  color: #b0b0b0;
  overflow: hidden;
}
.shoppingCart .cart-empty .empty h2 {
  margin: 70px 0 15px;
  font-size: 36px;
}
.shoppingCart .cart-empty .empty p {
  margin: 0 0 20px;
  font-size: 20px;
}
</style>