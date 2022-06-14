1. std::get<n>(), n从0开始。模板函数std::get<n>()是一个辅助函数，它能够获取到容器的第 n 个元素。
2. 查找函数:find()、find_if()、search() 等，这些函数的底层实现都采用的是顺序查找（逐个遍历）的方式，在某些场景中的执行效率并不高。当指定区域内的数据处于有序状态时，如果想查找某个目标元素，更推荐使用二分查找的方法，C++ STL标准库中还提供有 lower_bound()、upper_bound()、equal_range() 以及 binary_search() 这 4 个查找函数，它们的底层实现采用的都是二分查找的方式。
  1. lower_bound() 函数用于在指定区域内查找不小于目标值的第一个元素。
3. "std::unique_ptr<T,Deleter>"相关函数：
  1. reset():  Takes ownership of the pointer parameter, and then deletes the original stored pointer. If the new pointer is the same as the original stored pointer, reset deletes the pointer and sets the stored pointer to nullptr.
  2. get():  returns a pointer to the managed object(public member function).
4. 

