import 'package:praticesig/domain/user/user_provider.dart';

class UserRepository {
  final UserProvider _userProvider = UserProvider();

  Future<int> postUserName(String name, String d_num) async {
    final response = await _userProvider.postUserNamePage(name, d_num);
    if (response.statusCode == 200) {
      return 1;
    } else {
      throw Exception('Failed to create');
    }
  }
}
