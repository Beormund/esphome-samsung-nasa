#pragma once

#include "esphome/core/application.h"
#include <iostream>
#include <queue>

namespace esphome {
namespace samsung_nasa {

template<typename T> class LimitedQueue {
 public:
  explicit LimitedQueue(const size_t limit) : max_size_(limit) {}
  void push(const T &value) {
    if (this->queue_.size() >= this->max_size_)
      return;
    queue_.push(value);
  }
  T &front() { return this->queue_.front(); }
  const T &front() const { return this->queue_.front(); }
  T &back() { return this->queue_.back(); }
  const T &back() const { return this->queue_.back(); }
  void pop() { this->queue_.pop(); }
  bool empty() const { return this->queue_.empty(); }
  size_t size() const { return this->queue_.size(); }

 protected:
  std::queue<T> queue_;
  const size_t max_size_;
};

template<typename T> class BatchDispatcher {
 public:
  BatchDispatcher(const size_t limit, const size_t batch, const size_t delay)
      : limited_queue_{limit}, batch_size_{batch}, delay_{delay} {}
  using RegisterReceiveFunc = std::function<void(std::vector<T>)>;
  void register_receive_callback(RegisterReceiveFunc rrf) { this->receiveFunc_ = rrf; }
  void setup() { this->last_receive_ = millis(); }
  void push(const T value) { this->limited_queue_.push(value); }
  void push(const std::vector<T> values ) {
    for (const auto& value : values) {
        this->push(value);
    }
  }
  void update() {
    auto now = millis();
    if ((now - this->last_receive_) >= this->delay_) {
      this->dispatch();
      this->last_receive_ = now;
    }
  }

 protected:
  void dispatch() {
    size_t items_to_pop = std::min(this->limited_queue_.size(), this->batch_size_);
    if (items_to_pop == 0)
      return;
    std::vector<T> messages;
    for (size_t i = 0; i < items_to_pop; ++i) {
      if (!this->limited_queue_.empty()) {
        messages.push_back(this->limited_queue_.front());
        this->limited_queue_.pop();
      }
    }
    this->receiveFunc_(messages);
  };
  LimitedQueue<T> limited_queue_;
  const size_t batch_size_;
  const size_t delay_;
  uint32_t last_receive_{0};
  RegisterReceiveFunc receiveFunc_ = [](std::vector<T> v) -> void {};
};

}  // namespace samsung_nasa
}  // namespace esphome
